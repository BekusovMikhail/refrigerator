import cv2
import numpy as np
import tritonclient.http as httpclient
import mmcv
from tracker import TrackState
import argparse
from PIL import Image, ImageDraw, ImageFont
import os
from classes_names import classes_names



def img_detector_preprocess(image, dim=(640, 640)):
    shape = image.shape[:2]
    scale_factor = 640 / max(shape)
    image = mmcv.imrescale(
        img=image,
        scale=scale_factor,
        interpolation="area" if scale_factor < 1 else "bilinear",
    )
    new_shape = image.shape[:2]
    padding_h, padding_w = [dim[0] - image.shape[0], dim[1] - image.shape[1]]
    top_padding, left_padding = int(round(padding_h // 2 - 0.1)), int(
        round(padding_w // 2 - 0.1)
    )
    bottom_padding = padding_h - top_padding
    right_padding = padding_w - left_padding

    padding_list = [top_padding, bottom_padding, left_padding, right_padding]
    image = mmcv.impad(
        img=image,
        padding=(padding_list[2], padding_list[0], padding_list[3], padding_list[1]),
        pad_val=(114, 114, 114),
        padding_mode="constant",
    )
    img_preprocessed = image.transpose(2, 0, 1)
    img_preprocessed = img_preprocessed.astype("float32") / 255.0
    img_preprocessed = np.expand_dims(img_preprocessed, axis=0)
    return img_preprocessed, {
        "shape": shape,
        "new_shape": new_shape,
        "padding_list": padding_list,
    }


def img_classificator_preprocess(image, dim=(224,224)):
    img_preprocessed = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    img_preprocessed = img_preprocessed.transpose(2,0,1)
    img_preprocessed = img_preprocessed.astype('float32')/255.0
    img_preprocessed = np.expand_dims(img_preprocessed, axis=0)
    return img_preprocessed


def filter_boxes(boxes, scores, labels, shapes_info, score_thr=0.4):
    filtered_boxes = []
    filtered_scores = []
    filtered_labels = []
    for i in range(len(boxes)):
        if scores[i] > score_thr:
            tb = [
                shapes_info["shape"][1] * (boxes[i][0] - shapes_info["padding_list"][2]) / shapes_info["new_shape"][1],
                shapes_info["shape"][0] * (boxes[i][1] - shapes_info["padding_list"][0]) / shapes_info["new_shape"][0],
                shapes_info["shape"][1] * (boxes[i][2] - shapes_info["padding_list"][2]) / shapes_info["new_shape"][1],
                shapes_info["shape"][0] * (boxes[i][3] - shapes_info["padding_list"][0]) / shapes_info["new_shape"][0],
            ]
            tb[0] = 0 if tb[0] < 0 else tb[0]
            tb[1] = 0 if tb[1] < 0 else tb[1]
            tb[2] = 0 if tb[2] < 0 else tb[2]
            tb[3] = 0 if tb[3] < 0 else tb[3]
            # tb = [tb[0], tb[1], tb[2]-tb[0], tb[3]-tb[1]]
            filtered_boxes.append(tb)
            filtered_scores.append(scores[i])
            filtered_labels.append(labels[i])

    return filtered_boxes, filtered_scores, filtered_labels


def find_objects(boxes, scores, labels, shapes_info):
    hand_obj_ids = [i for i, l in enumerate(labels) if l in [1, 2]]
    hand_scr_max = -1
    best_hand_id = None
    for i in hand_obj_ids:
        if scores[i] > hand_scr_max:
            hand_scr_max = scores[i]
            best_hand_id = i

    obj_ids = [i for i, l in enumerate(labels) if l == 0]
    obj_scr_max = -1
    best_obj_id = None
    for i in obj_ids:
        if scores[i] > obj_scr_max:
            obj_scr_max = scores[i]
            best_obj_id = i

    result = {"hand": None, "object": None}
    if best_hand_id is None:
        result["status"] = 0

    else:
        result["hand"] = {
            "bbox": boxes[best_hand_id],
            "score": scores[best_hand_id],
            "label": labels[best_hand_id],
        }
        if best_obj_id is not None:
            if labels[best_hand_id] == 1:
                result["status"] = 1
            else:
                result["status"] = 2
            result["object"] = {
                "bbox": boxes[best_obj_id],
                "score": scores[best_obj_id],
                "label": labels[best_obj_id],
            }
        else:
            if labels[best_hand_id] == 1:
                result["status"] = 3
            else:
                result["status"] = 4

    return result

def get_detection_res(client, img_preprocessed):
    detection_input = httpclient.InferInput("images", img_preprocessed.shape, datatype="FP32")
    detection_input.set_data_from_numpy(img_preprocessed, binary_data=True)
    detection_response = client.infer(model_name="hand_detection", inputs=[detection_input])
    boxes = detection_response.as_numpy('boxes')[0]
    scores = detection_response.as_numpy('scores')[0]
    labels = detection_response.as_numpy('labels')[0]
    return boxes, scores, labels


def get_classification_res(client, img_preprocessed):
    detection_input = httpclient.InferInput("input", img_preprocessed.shape, datatype="FP32")
    detection_input.set_data_from_numpy(img_preprocessed, binary_data=True)
    outputs = client.infer(model_name="classification", inputs=[detection_input])
    out = outputs.as_numpy('output')[0]
    return out


def get_image_with_boxes_ind(img, boxes):
    image_for_draw = img
    image_for_draw = Image.fromarray(np.uint8(img)).convert("RGB")

    draw = ImageDraw.Draw(image_for_draw)

    for i in range(len(boxes)):
        draw.rectangle(
            [(boxes[i][0], boxes[i][1]), (boxes[i][2], boxes[i][3])],
            outline=(0, 255, 0),
            width=2,
        )

    return np.array(image_for_draw)

def main(args):

    cap = cv2.VideoCapture(
        args.vid_path
    )

    width = cap.get(3)
    height = cap.get(4)

    if (cap.isOpened()== False): 
        print("Error opening video stream or file")


    frame_counter = 0
    imgs = []

    cam_direction = 0 if args.hand_direction == 'Hor' else 1

    fridge_side = False if args.fridge_side == 'Left' else True

    tracker = TrackState(cam_direction=cam_direction)

    statuses = {
        0: "No hands",
        1: "Hand with object",
        2: "Object detected, hand empty",
        3: "Object not detected, hand with object",
        4: "Empty hand",
    }

    client = httpclient.InferenceServerClient(url="127.0.0.1:8000")

    final_tracking_results = []

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            imgs.append(frame)
            img_preprocessed, shapes_info = img_detector_preprocess(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            boxes, scores, labels = get_detection_res(client, img_preprocessed)
            filtered_boxes, filtered_scores, filtered_labels = filter_boxes(boxes, scores, labels, shapes_info)
            objs = find_objects(filtered_boxes, filtered_scores, filtered_labels, shapes_info)

            result = tracker.update(objs, frame_counter)

            if result is not None:

                max_obj_conf = -1
                max_obj_id = -1
                for i in range(result[0], result[1]):
                    obj = tracker.frame_objects[i]
                    if obj['object'] is not None and obj['object']['score'] > max_obj_conf:
                        max_obj_conf = obj['object']['score']
                        max_obj_id = i

                obj = tracker.frame_objects[max_obj_id]
        
                img_cropped = imgs[max_obj_id][int(obj['object']['bbox'][1]):int(obj['object']['bbox'][3]), int(obj['object']['bbox'][0]):int(obj['object']['bbox'][2]),  :]
                img_preprocessed = img_classificator_preprocess(cv2.cvtColor(img_cropped, cv2.COLOR_BGR2RGB))
                scores = get_classification_res(client, img_preprocessed)
                name = classes_names[np.argmax(scores)]
                action = 'add' if result[2] == fridge_side else 'rm'
                final_tracking_results.append({
                    'action': action,
                    'name': name
                })

            frame_counter += 1
        else: 
            break
    
    cap.release()

    for res in final_tracking_results:
        if res['action'] == 'add':
            os.system(f"python add_rm_product_from_DB.py --product_name {res['name']} --fridge_id {args.fridge_id}")
        else:
            os.system(f"python add_rm_product_from_DB.py --product_name {res['name']} --rm --fridge_id {args.fridge_id}")
        # print(res)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Arguments for camera')
    parser.add_argument('-p','--vid_path', type=str, help='Video path', required=True)
    parser.add_argument('-i','--fridge_id', type=str, help='Fridge id', required=True)
    parser.add_argument('-d', '--hand_direction', type=str, help='hand_direction', choices=['Vert', 'Hor'], default='Hor')
    parser.add_argument('-f', '--fridge_side', type=str, help='hand_direction', choices=['Left', 'Right'], default='Left')


    args = parser.parse_args()
    main(args)
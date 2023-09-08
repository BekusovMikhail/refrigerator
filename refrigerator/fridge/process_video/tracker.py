

class TrackState:

    def __init__(self, cam_direction=0, num_frames_to_stop_track=3, num_frames_to_start_track=3, num_frames_to_clean_history=5) -> None:
        self.cam_direction = cam_direction # 0 = x, 1 = y
        self.num_frames_to_stop_track = num_frames_to_stop_track
        self.num_frames_to_start_track = num_frames_to_start_track
        self.num_frames_to_clean_history = num_frames_to_clean_history
        self.num_frames_to_change_dir = 3
        self.start_counter = 0
        self.stop_counter = 0
        self.change_counter = 0
        self.track_state = 0 # 0: Track not started, 1: Track Started
        self.start_track_frame_num = None
        self.frame_objects = []
        self.current_track_direction = None # True = +, False = -

        self.object_state_counter = 0 # < 0 obj, > 0 no obj 


    def count_diff(self, a, b):
        if self.cam_direction == 0:
            a = (self.frame_objects[a]['hand']['bbox'][0]+self.frame_objects[a]['hand']['bbox'][2])/2
            b = (self.frame_objects[b]['hand']['bbox'][0]+self.frame_objects[b]['hand']['bbox'][2])/2
        else:
            a = (self.frame_objects[a]['hand']['bbox'][1]+self.frame_objects[a]['hand']['bbox'][3])/2
            b = (self.frame_objects[b]['hand']['bbox'][1]+self.frame_objects[b]['hand']['bbox'][3])/2
        diff = b - a
        return diff

    # def __init_new_track__(self, )

    def update(self, objs, frame_num):
        
        self.frame_objects.append(objs)
        

        if objs['status'] == 0: # if hand not detected
            if self.track_state == 1:
                self.stop_counter += 1
                if self.stop_counter >= self.num_frames_to_stop_track:
                    output = None
                    if self.object_state_counter < -10:
                        output =  (self.start_track_frame_num, frame_num+1-self.num_frames_to_change_dir, self.current_track_direction, self.object_state_counter)
                    self.start_counter = 0
                    self.stop_counter = 0
                    self.change_counter = 0
                    self.track_state = 0
                    self.object_state_counter = 0
                    self.start_track_frame_num = None
                    self.current_track_direction = None
                    if output is not None:
                        return output
            elif self.track_state == 0:
                self.start_counter = 0
                    
            return None
        
        # if hand detected

        if self.track_state == 0:
            self.start_counter += 1
            if self.start_counter == self.num_frames_to_start_track:
                self.track_state = 1
                self.start_track_counter = 0
                diff = 0
                for i in range(-self.num_frames_to_start_track, -1, 1):
                    if self.frame_objects[i]['status'] in (1,2):
                        self.object_state_counter += objs['status']-3
                    elif self.frame_objects[i]['status'] in (3,4):
                        self.object_state_counter += objs['status']-2
                    t_diff = self.count_diff(i, i+1)
                    diff += t_diff

                self.current_track_direction = True if diff > 0 else False          
                self.start_track_frame_num = frame_num
                self.stop_counter = 0
                self.change_counter = 0
                
        elif self.track_state == 1:
            a = -2
            while self.frame_objects[a]['hand'] is None:
                a -= 1
            diff = self.count_diff(a, -1)
            diff = True if diff > 0 else False
            if diff != self.current_track_direction:
                self.change_counter += 1
                if self.change_counter >= self.num_frames_to_change_dir:
                   # finish track and change dir
                    output = None
                    if self.object_state_counter < -10:
                        output =  (self.start_track_frame_num, frame_num+1-self.num_frames_to_change_dir, self.current_track_direction, self.object_state_counter)
                    self.start_counter = 0
                    self.stop_counter = 0
                    self.change_counter = 0
                    self.track_state = 1
                    self.object_state_counter = 0
                    self.start_track_frame_num = frame_num
                    diff = 0
                    a = -2
                    b = -1
                    for i in range(self.num_frames_to_change_dir):
                        while self.frame_objects[a]['hand'] is None:
                            a -= 1
                        t_diff = self.count_diff(a, b)
                        diff += t_diff
                        b = a
                        a = a-1

                    self.current_track_direction = True if diff > 0 else False
                    if output is not None:
                        return output


            else:
                if objs['status'] in (1,2):
                    self.object_state_counter += objs['status']-3
                elif objs['status'] in (3,4):
                    self.object_state_counter += objs['status']-2
                self.change_counter = 0
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework.viewsets import ViewSet

from django.conf import settings

import subprocess

from .models import ExtendedUser, Counter, Camera, Product
from django.contrib.auth.models import User
from .serializers import (
    ProductSerializer,
    CameraSerializer,
    CounterSerializer,
    ExtendedUserSerializer,
    VideoSerializer,
)
import json

from django.views.decorators.csrf import csrf_exempt
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseForbidden,
    JsonResponse,
)
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
from django.core.files.base import ContentFile
from .models import *
import os
import json
import sys
import time
import cv2


class GetProducts(APIView):
    id = None

    def get(self, request, id=None):
        self.id = id
        if self.id:
            queryset = Product.objects.get(pk=self.id)
            serializer_for_queryset = ProductSerializer(instance=queryset, many=False)
        else:
            queryset = Product.objects.all()
            serializer_for_queryset = ProductSerializer(instance=queryset, many=True)
        return Response(serializer_for_queryset.data)


class GetCameras(APIView):
    id = None

    def get(self, request, id=None):
        self.id = id
        if self.id:
            queryset = Camera.objects.get(pk=self.id)
            serializer_for_queryset = CameraSerializer(instance=queryset, many=False)
        else:
            queryset = Camera.objects.all()
            serializer_for_queryset = CameraSerializer(instance=queryset, many=True)
        return Response(serializer_for_queryset.data)


class GetUsers(APIView):
    id = None

    def get(self, request, id=None):
        self.id = id
        if self.id:
            queryset = ExtendedUser.objects.get(pk=self.id)
            serializer_for_queryset = ExtendedUserSerializer(
                instance=queryset, many=False
            )
        else:
            queryset = ExtendedUser.objects.all()
            serializer_for_queryset = ExtendedUserSerializer(
                instance=queryset, many=True
            )
        return Response(serializer_for_queryset.data)


class GetCounters(APIView):
    id = None

    def get(self, request, id=None):
        self.id = id
        if self.id:
            queryset = Counter.objects.get(pk=self.id)
            serializer_for_queryset = CounterSerializer(instance=queryset, many=False)
        else:
            queryset = Counter.objects.all()
            serializer_for_queryset = CounterSerializer(instance=queryset, many=True)
        return Response(serializer_for_queryset.data)


class GetCamerasByUser(APIView):
    id = None

    def get(self, request, id=None):
        self.id = id
        if self.id:
            queryset = Camera.objects.filter(user=self.id)
            serializer_for_queryset = CameraSerializer(instance=queryset, many=True)
        return Response(serializer_for_queryset.data)


class GetCamerasByUserUsername(APIView):
    username = None

    def get(self, request, username=None):
        self.username = username
        print(username)
        if self.username:
            user = User.objects.filter(username=self.username)[0]
            print(user)
            queryset = Camera.objects.filter(user=user.id)
            serializer_for_queryset = CameraSerializer(instance=queryset, many=True)
        return Response(serializer_for_queryset.data)


class GetCountersByCamera(APIView):
    id = None

    def get(self, request, id=None):
        self.id = id
        if self.id:
            queryset = Counter.objects.filter(camera=self.id, current_counter__gt=0)
            serializer_for_queryset = CounterSerializer(instance=queryset, many=True)
            return Response(serializer_for_queryset.data)


class GetCountersByProduct(APIView):
    id = None

    def get(self, request, id=None):
        self.id = id
        if self.id:
            queryset = Counter.objects.filter(product=self.id)
            serializer_for_queryset = CounterSerializer(instance=queryset, many=True)
            return Response(serializer_for_queryset.data)


@csrf_exempt
def loginUser(request):
    if request.method == "POST" and request.content_type == "application/json":
        try:
            data = json.loads(request.body)
            username = data["username"]
            password = data["password"]
            rememberMe = data["rememberMe"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if not rememberMe:
                    request.session.set_expiry(0)
                return JsonResponse(
                    {"success": True, "message": "User authenticated successfully"}
                )
            else:
                return JsonResponse(
                    {"success": False, "message": "Invalid username or password"}
                )
        except:
            return JsonResponse(
                {
                    "success": False,
                    "message": "An error occurred while authenticating user",
                }
            )
    else:
        return JsonResponse({"success": False, "message": "Invalid request method"})


@csrf_exempt
def regUser(request):
    if request.method == "POST" and request.content_type == "application/json":
        data = json.loads(request.body)

        username = data["username"]
        password = data["password"]
        email = data["email"]
        first_name = data["name"]
        last_name = data["surname"]

        new_user = User.objects.create_user(username, email, password)
        new_user.first_name = first_name
        new_user.last_name = last_name

        new_user.save()

        ext_user = ExtendedUser(user=new_user)
        if "patronymic" in data:
            ext_user.patronymic = data["patronymic"]
        ext_user.save()

        login(request, new_user)

        response_data = {"success": True, "message": "User registered successfully"}

        return JsonResponse(response_data)
    else:
        response_data = {"success": False, "message": "Only POST requests are allowed"}

        return JsonResponse(response_data, status=405)


@csrf_exempt
def create_camera(request):
    if request.method == "POST" and request.content_type == "application/json":

        import psycopg2

        conn = psycopg2.connect(
            host="127.0.0.1",
            database="refrigeratorDB",
            user="refrigeratorUser",
            password="rupass",
        )
        cur = conn.cursor()

        data = json.loads(request.body)

        name = data["name"]
        url = data["url"]
        try:
            user_tmp = User.objects.filter(username=data['username'])[0]
            user_tmp = ExtendedUser.objects.get(pk=user_tmp.id)
        except:
            response_data = {
                "success": False,
                "message": "This user doesn't exist",
            }

            return JsonResponse(response_data, status=400)

        # print(dir(request))
        # print(dir(request.user))
        # print(request.user.pk, request.user.username)
        new_camera = Camera.objects.create(
            url=url, user=user_tmp, name=name
        )
        new_camera.status = 0
        new_camera.save()

        products = Product.objects.all()
        for prod in products:
            counter = Counter.objects.create(
                camera = new_camera,
                product = prod,
            )

        # try:
        #     cap = cv2.VideoCapture(new_camera.url)
        #     ret, frame = cap.read()
        #     if not ret:
        #         raise Exception("Cannot read stream")
        #     ret, buf = cv2.imencode(".jpg", frame)
        #     if not ret:
        #         raise Exception("Cannot read stream")
        #     content = ContentFile(buf.tobytes())
        #     new_camera.sample_image.save(
        #         "sample_image_{}.jpg".format(new_camera.id), content
        #     )

        # except:
        #     response_data = {
        #         "success": False,
        #         "message": "Error reading from videostream",
        #     }

        #     return JsonResponse(response_data, status=400)

        response_data = {
            "success": True,
            "message": "Camera was added successfully",
            "cam_id": new_camera.id,
        }

        return JsonResponse(response_data)

    # handle other request methods
    else:
        response_data = {"success": False, "message": "Only POST requests are allowed"}

        return JsonResponse(response_data, status=405)


#@login_required
@csrf_exempt
def delete_camera(request):
    if request.method == "POST" and request.content_type == "application/json":
        # parse json data from request
        data = json.loads(request.body)

        id = int(data["id"])
        print(Camera.objects.filter(id=id))
        print(Camera.objects.filter(id=id)[0].pid)

        # taskkill /PID <pid> /F
        #os.system(f"taskkill /PID {Camera.objects.filter(id=id)[0].pid} /F")
        Camera.objects.filter(id=id).delete()

        response_data = {"success": True, "message": "Camera was deleted successfully"}

        return JsonResponse(response_data)

    # handle other request methods
    else:
        response_data = {"success": False, "message": "Only POST requests are allowed"}

        return JsonResponse(response_data, status=405)


@login_required
@csrf_exempt
def reset_all_counters(request):
    if request.method == "POST" and request.content_type == "application/json":
        # parse json data from request
        data = json.loads(request.body)

        id = data["id"]

        try:
            obj = Camera.objects.get(pk=id)
            counters = Counter.objects.filter(camera=obj.id)
            for cou in counters:
                cou.current_counter = 0
                cou.save()

            response_data = {"success": True, "message": "Счетчики успешно сброшены"}
        except Exception as exc:
            response_data = {
                "success": False,
                "message": "Ошибка при обновлении счетчиков",
            }

        return JsonResponse(response_data)

    # handle other request methods
    else:
        response_data = {"success": False, "message": "Only POST requests are allowed"}

        return JsonResponse(response_data, status=405)


@login_required
@csrf_exempt
def launch_camera_process(request):
    if request.method == "POST" and request.content_type == "application/json":
        data = json.loads(request.body)

        id = data["id"]
        obj = Camera.objects.get(pk=id)
        command = None  ##################################
        # sf = subprocess.Popen(command) #######
        obj.pid = None  #################
        # obj.pid = sf.pid
        obj.status = 2
        obj.current_counter = 0
        obj.save()
        response_data = {"success": True, "message": "Удалось запустить камеру"}

        return JsonResponse(response_data)

    else:
        response_data = {"success": False, "message": "Only POST requests are allowed"}

        return JsonResponse(response_data, status=405)


@login_required
@csrf_exempt
def stop_camera_process(request):
    if request.method == "POST" and request.content_type == "application/json":
        # parse json data from request
        data = json.loads(request.body)

        try:
            id = data["id"]
            obj = Camera.objects.get(pk=id)
            if obj.status != 2:
                return JsonResponse(response_data)
            os.system(f"taskkill /PID {Camera.objects.get(pk=id).pid} /F")
            obj.pid = None
            obj.status = 1
            obj.current_counter = 0
            obj.save()
            response_data = {"success": True, "message": "Камера остановлена"}
        except:
            response_data = {
                "success": False,
                "message": "Не удалось остановить камеру",
            }
            print("Не удалось запустить камеру")

        return JsonResponse(response_data)

    else:
        response_data = {"success": False, "message": "Only POST requests are allowed"}

        return JsonResponse(response_data, status=405)


@csrf_exempt
def add_counter(request):
    if request.method == "POST" and request.content_type == "application/json":
        data = json.loads(request.body)

        #try:
        camera_id = int(data["camera_id"])
        product_id = data["product_id"]
        print(camera_id, product_id)

        new_counter = Counter.objects.create(
            camera=Camera.objects.get(pk=camera_id),
            product=Product.objects.get(pk=product_id),
        )
        new_counter.save()
        response_data = {"success": True, "message": "Counter добавлен"}
        # except:
        #     response_data = {
        #         "success": False,
        #         "message": "Не удалось добавить Counter",
        #     }

        return JsonResponse(response_data)

    else:
        response_data = {"success": False, "message": "Only POST requests are allowed"}

        return JsonResponse(response_data, status=405)


@login_required
@csrf_exempt
def add_product(request):
    if request.method == "POST" and request.content_type == "application/json":
        data = json.loads(request.body)

        try:
            name = data["name"]

            new_product = Product.objects.create(
                name=name,
            )
            new_product.save()
            response_data = {"success": True, "message": "Product добавлен"}
        except:
            response_data = {
                "success": False,
                "message": "Не удалось добавить Product",
            }

        return JsonResponse(response_data)

    else:
        response_data = {"success": False, "message": "Only POST requests are allowed"}

        return JsonResponse(response_data, status=405)


class DeleteProduct(APIView):
    id = None

    def get(self, request, id=None):
        self.id = id
        if self.id:
            product = Product.objects.get(pk=self.id)
            ret_product = Product.objects.get(pk=self.id)
            product.delete()
            serializer_for_queryset = ProductSerializer(
                instance=ret_product, many=False
            )
            return Response(serializer_for_queryset.data)
        else:
            return None


class DeleteCounter(APIView):
    id = None

    def get(self, request, id=None):
        self.id = id
        if self.id:
            counter = Counter.objects.get(pk=self.id)
            ret_counter = Counter.objects.get(pk=self.id)
            counter.delete()
            serializer_for_queryset = CounterSerializer(
                instance=ret_counter, many=False
            )
            return Response(serializer_for_queryset.data)
        else:
            return None


class VideoViewSet(ViewSet):
    serializer_class = VideoSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):        
        try:
            upload_file = request.FILES.get("upload_file")
            data = request.data
            #print(data)
            try:
                hand_direction = data["hand_direction"]
            except:
                hand_direction='Hor'
            try:
                fridge_side = data["fridge_side"]
            except:
                fridge_side='Right'
            video_cam = Camera.objects.get(pk=int(data["camera"]))
            video = Video(
                name=data["name"],
                user=video_cam.user,
                camera=video_cam,
                video=upload_file,
            )
            video.save()
            print(data["hand_direction"])
            print(settings.BASE_DIR)
            subprocess_command = [
                "python",
                os.path.join(settings.BASE_DIR, "fridge/process_video/process_vid_cmd.py"),
                "--vid_path",
                os.path.join(settings.BASE_DIR, "media", video.video.__str__()),
                "--fridge_id",
                str(int(data["camera"][0])),
                "--hand_direction",
                hand_direction,
                "--fridge_side",
                fridge_side,
            ]
            subprocess.run(subprocess_command)
            content_type = upload_file.content_type
            response = "You have uploaded a {} file".format(content_type)
        except:
            response = "Bad fields"
        return Response(response)

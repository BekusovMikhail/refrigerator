from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ExtendedUser, Counter, Camera, Product
from django.contrib.auth.models import User
from .serializers import (
    ProductSerializer,
    CameraSerializer,
    CounterSerializer,
    ExtendedUserSerializer,
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
import subprocess
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


class GetCountersByCamera(APIView):
    id = None

    def get(self, request, id=None):
        self.id = id
        if self.id:
            queryset = Counter.objects.filter(camera=self.id)
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
@login_required
def create_camera(request):
    if request.method == "POST" and request.content_type == "application/json":
        data = json.loads(request.body)

        name = data["name"]
        url = data["url"]
        model = data["model"]

        new_camera = Camera.objects.create(
            url=url, model=model, user=request.user.origin_user, name=name
        )
        new_camera.status = 0
        new_camera.save()

        try:
            cap = cv2.VideoCapture(new_camera.url)
            ret, frame = cap.read()
            if not ret:
                raise Exception("Cannot read stream")
            ret, buf = cv2.imencode(".jpg", frame)
            if not ret:
                raise Exception("Cannot read stream")
            content = ContentFile(buf.tobytes())
            new_camera.sample_image.save(
                "sample_image_{}.jpg".format(new_camera.id), content
            )

        except:
            response_data = {
                "success": False,
                "message": "Error reading from videostream",
            }

            return JsonResponse(response_data, status=400)

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


@login_required
@csrf_exempt
def delete_camera(request):
    if request.method == "POST" and request.content_type == "application/json":
        # parse json data from request
        data = json.loads(request.body)

        id = data["id"]
        print(Camera.objects.filter(id=id))
        print(Camera.objects.filter(id=id)[0].pid)

        # taskkill /PID <pid> /F
        os.system(f"taskkill /PID {Camera.objects.filter(id=id)[0].pid} /F")
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

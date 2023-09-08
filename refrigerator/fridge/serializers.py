from rest_framework import serializers, renderers
from rest_framework.serializers import FileField, CharField
from .models import Video


class ExtendedUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="user.id")
    last_login = serializers.DateTimeField(source="user.last_login")
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    date_joined = serializers.DateTimeField(source="user.date_joined")
    phone = serializers.CharField(max_length=20)
    patronymic = serializers.CharField(max_length=30)
    is_admin = serializers.BooleanField(default=False)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)


class CameraSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    url = serializers.CharField(max_length=100)
    user = serializers.IntegerField(source="user.user.id")
    description = serializers.CharField(max_length=400)
    creationDate = serializers.DateTimeField()
    pid = serializers.IntegerField()
    status = serializers.IntegerField()


class CounterSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_id = serializers.IntegerField(source="product.id")
    current_counter = serializers.IntegerField()
    camera_id = serializers.IntegerField(source="camera.id")


class VideoSerializer(serializers.ModelSerializer):
    upload_file = FileField()
    hand_direction = fridge_side = serializers.ChoiceField(
        choices=["Hor", "Vert"], style={"base_template": "radio.html"},
    )
    fridge_side = serializers.ChoiceField(
        choices=["Left", "Right"], style={"base_template": "radio.html"},
    )

    class Meta:
        model = Video
        fields = ["name", "camera", "hand_direction", "fridge_side", "upload_file"]

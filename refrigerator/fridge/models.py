from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class ExtendedUser(models.Model):
    phone = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=30)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key = True,
        related_name='origin_user')
    is_admin = models.BooleanField(default=False)
    creationDate = models.DateTimeField(auto_now_add=True)

class Counter(models.Model):
    product = models.ForeignKey('ExtendedUser', on_delete=models.CASCADE)
    current_counter = models.IntegerField(default=0)

class Camera(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    url = models.CharField(max_length=100, null=False, blank=False)
    user = models.ForeignKey('ExtendedUser', on_delete=models.CASCADE)
    description = models.CharField(max_length=400, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    pid = models.IntegerField(default=None, null=True)
    status = models.IntegerField(default=0)
    # sample_image = models.FileField(upload_to='sample_images/', null=True)

class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

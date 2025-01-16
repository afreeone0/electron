from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=20)
    image = models.ImageField(upload_to='users_images', null=True, blank=True)

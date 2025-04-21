from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_obj = User.objects.get(pk=self.pk)
            if self.image and old_obj.image != self.image:
                old_obj.image.delete(save=False)
        super().save(*args, **kwargs)

from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from .models import User
from django import forms
from validators import get_validators_list
from PIL import Image
import logging
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.fields.files import ImageFieldFile

logger = logging.getLogger('users_logger')


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={}), required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={}))
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'readonly': True}))

    def get_params_of_a_cropped_square(self, width, height):
        pivot = min(width, height)
        x = (width - height) // 2
        x = x if x >= 0 else 0
        y = (height - width) // 2
        y = y if y >= 0 else 0
        z = x + pivot
        w = y + pivot
        logging.debug(f'params of a square: {x}, {y}, {z}, {w}')
        return x, y, z, w

    def round_image(self, img, **kwargs):
        logger.debug('inside round_image func')
        given = Image.open(img)
        logger.debug(f'opened the image, its size: {given.size}')
        cropped = given.crop(self.get_params_of_a_cropped_square(*given.size))
        logger.debug('cropped that')
        resized = cropped.resize((200, 200))
        logger.debug('resized that')
        buffer = BytesIO()
        img_format = img.name[img.name.find('.') + 1:]
        logger.debug(f'image format = {img_format}')
        resized.save(fp=buffer, quality=100, format=img_format)
        image_content_file = ContentFile(content=buffer.getvalue())
        return InMemoryUploadedFile(image_content_file, **kwargs)

    def clean_image(self):
        logger.info('cleaning an image')
        image = self.cleaned_data['image']
        logger.debug(f'got the image, type: {type(image)}')
        if not isinstance(image, ImageFieldFile):
            for validator in get_validators_list():
                validator(image)
            logger.debug('validated the image')
            kwargs = {
                'charset': image.charset,
                'content_type': image.content_type,
                'field_name': image.field_name,
                'name': image.name,
                'size': image.size
            }
            image = self.round_image(image, **kwargs)
            logger.info(f'rounded the image user sent. image was cleaned, type: {type(image)}\n')
        return image

    class Meta:
        model = User
        fields = ('image', 'first_name', 'last_name', 'username', 'email')

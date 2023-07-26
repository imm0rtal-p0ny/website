import datetime
import os
import uuid
from io import BytesIO
from django.conf import settings
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from user.models import CustomUser
from django.core.files.storage import default_storage
from PIL import Image, ImageOps
from django.core.files.base import ContentFile


DEFAULT_BOARD_PHOTO = 'photo_default.png'
DEFAULT_BOARD_PHOTO_ICON = 'photo_default_icon.png'
DEFAULT_BOARD_PHOTO_PAGE = 'photo_default_page.png'


def delete_photos_except_default(board):
    if board.photo.name != DEFAULT_BOARD_PHOTO:
        default_storage.delete(board.photo.name)
    if board.photo_icon.name != DEFAULT_BOARD_PHOTO_ICON:
        default_storage.delete(board.photo_icon.name)
    if board.photo_page.name != DEFAULT_BOARD_PHOTO_PAGE:
        default_storage.delete(board.photo_page.name)


def board_photo_upload_path(instance, filename):
    _, ext = os.path.splitext(filename)
    unique_filename = f'{uuid.uuid4().hex}{datetime.datetime.now()}{ext}'
    return f'{unique_filename}'


def board_photo_icon_upload_path(instance, filename):
    name, ext = os.path.splitext(instance.photo.name)

    return f'{name}_icon{ext}'


def board_photo_page_upload_path(instance, filename):
    name, ext = os.path.splitext(instance.photo.name)

    return f'{name}_page{ext}'


def default_photo(photo, size):
    if photo == DEFAULT_BOARD_PHOTO:
        if size == (100, 100):
            return DEFAULT_BOARD_PHOTO_ICON
        if size == (300, 300):
            return DEFAULT_BOARD_PHOTO_PAGE

    image = Image.open(photo)
    image.thumbnail(size)
    padded_image = ImageOps.pad(image, size)
    buffer = BytesIO()
    padded_image.save(buffer, format='PNG')
    image_data = buffer.getvalue()

    image_file = InMemoryUploadedFile(
        file=BytesIO(image_data),
        field_name=None,
        name='111111.png',
        content_type='image/png',
        size=len(image_data),
        charset=None
    )

    return image_file


class Board(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=150)
    view_count = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    photo = models.ImageField(upload_to=board_photo_upload_path, default=DEFAULT_BOARD_PHOTO, null=False)
    photo_icon = models.ImageField(upload_to=board_photo_icon_upload_path, null=False)
    photo_page = models.ImageField(upload_to=board_photo_page_upload_path, null=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)
    division = models.ForeignKey('Division', on_delete=models.CASCADE)
    condition = models.ForeignKey('Condition', on_delete=models.CASCADE)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.photo_icon:
            self.photo_icon = default_photo(self.photo, (100, 100))
        if not self.photo_page:
            self.photo_page = default_photo(self.photo, (300, 300))
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        delete_photos_except_default(self)

        super().delete(using=using, keep_parents=keep_parents)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def update_photo(self, old_photo=None, is_api=False, clear_photo=False):
        if clear_photo:
            delete_photos_except_default(self)
            self.photo = DEFAULT_BOARD_PHOTO
            self.photo_page = None
            self.photo_icon = None
            self.save()

        elif old_photo != self.photo:
            delete_photos_except_default(self)
            if is_api:
                self.photo = old_photo
            else:
                if old_photo != DEFAULT_BOARD_PHOTO:
                    default_storage.delete(old_photo.name)
            self.photo_page = None
            self.photo_icon = None
            self.save()


class Status(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    @staticmethod
    def get_choices_filter():
        result = [(None, '----')]
        for item in Region.objects.all():
            result.append((item.name, item.name))
        return result


class Division(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    @staticmethod
    def get_choices_filter():
        result = [(None, '----')]
        for item in Division.objects.all():
            result.append((item.name, item.name))
        return result

    @staticmethod
    def get_by_name(division_name):
        return Division.objects.get(name=division_name) if Division.objects.filter(name=division_name) else None


class Condition(models.Model):
    name = models.CharField(max_length=30, unique=True)

    @staticmethod
    def get_choices_filter():
        result = [(None, '----')]
        for item in Condition.objects.all():
            result.append((item.name, item.name))
        return result

    def __str__(self):
        return self.name
















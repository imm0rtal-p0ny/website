import datetime
from django.db import models
from user.models import CustomUser
from django.core.files.storage import default_storage
import os
import uuid


DEFAULT_BOARD_PHOTO = 'board_photos/photo_default.png'
DEFAULT_BOARD_PHOTO_ICON = 'board_photos/photo_default_icon.png'
DEFAULT_BOARD_PHOTO_PAGE = 'board_photos/photo_default_page.png'


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
    return f'board_photos/{unique_filename}'


def board_photo_icon_upload_path(instance, filename):
    name, ext = os.path.splitext(filename)

    return f'board_photos/{name}_icon{ext}'


def board_photo_page_upload_path(instance, filename):
    name, ext = os.path.splitext(filename)

    return f'board_photos/{name}_page{ext}'


class Board(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=150)
    view_count = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    photo = models.ImageField(upload_to=board_photo_upload_path, default=DEFAULT_BOARD_PHOTO, null=True)
    photo_icon = models.ImageField(upload_to=board_photo_icon_upload_path, default=DEFAULT_BOARD_PHOTO_ICON, null=True)
    photo_page = models.ImageField(upload_to=board_photo_page_upload_path, default=DEFAULT_BOARD_PHOTO_PAGE, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)
    division = models.ForeignKey('Division', on_delete=models.CASCADE)
    condition = models.ForeignKey('Condition', on_delete=models.CASCADE)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


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
















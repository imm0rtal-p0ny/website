import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import hashlib
import random
import string
from django.utils import timezone
from .user_exception import NotUserException, NotUserCodeException, TimeOutCodeException, CodeDoNotMatchException, EmailAlreadyRegistered


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')

        user = CustomUser.objects.create(email=email, password=password, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    middle_name = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(editable=False, auto_now=datetime.datetime.now(), verbose_name='User created')
    updated_at = models.DateTimeField(editable=False, auto_now=datetime.datetime.now(), verbose_name='User update')
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_authorized = models.BooleanField(default=False)
    _code = models.ForeignKey('ConfirmationCode', on_delete=models.SET_NULL, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='customuser'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_query_name='customuser'
    )

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @staticmethod
    def get_by_email(email):
        custom_user = CustomUser.objects.filter(email=email).first()
        return custom_user if custom_user else None

    @staticmethod
    def verification(user_email):
        user = CustomUser.get_by_email(user_email)
        if user:
            user.is_authorized = True
            user.save()

            return True

        return False

    def update(self, **kwargs):
        if kwargs.get('first_name'):
            self.first_name = kwargs.get('first_name')
        if kwargs.get('last_name'):
            self.last_name = kwargs.get('last_name')
        if kwargs.get('middle_name'):
            self.middle_name = kwargs.get('middle_name')

        self.save()

    def update_email(self, new_email):
        is_not_email = CustomUser.get_by_email(new_email)
        if is_not_email or new_email == self.email:
            raise EmailAlreadyRegistered

        self.email = new_email
        self.is_authorized = False
        self.save()

        return True


class ConfirmationCode(models.Model):
    _code = models.CharField(max_length=7)
    created_at = models.DateTimeField(auto_now=datetime.datetime.now(), verbose_name='code created')

    @staticmethod
    def created_code(user_email):
        characters = string.digits + string.ascii_letters
        random_code = ''.join(random.choice(characters) for _ in range(5))
        hash_object = hashlib.md5()
        hash_object.update(random_code.encode())
        encrypted_code = hash_object.hexdigest()
        user = CustomUser.get_by_email(user_email)
        if not user:
            raise NotUserException(user_email)
        if user._code:
            user._code.delete()
        code_in = ConfirmationCode.objects.create(_code=encrypted_code)
        user._code = code_in
        user.save()

        return random_code



    @staticmethod
    def check_valid_code(user_email, code):
        user = CustomUser.get_by_email(user_email)
        hashed_code = hashlib.md5(code.encode()).hexdigest()
        time_now = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
        if not user:
            raise NotUserException(user_email)
        if not user._code:

            raise NotUserCodeException
        time_difference = time_now - user._code.created_at
        if hashed_code != user._code._code:

            raise CodeDoNotMatchException
        if time_difference.total_seconds() > 500:
            user._code.delete()
            raise TimeOutCodeException

        return True










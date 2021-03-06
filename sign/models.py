from uuid import uuid4
# Django imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Role(models.Model):
    role = models.CharField(max_length=30)


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(_('first name'), max_length=64, blank=False, null=True)
    last_name = models.CharField(_('last name'), max_length=64, blank=False, null=True)
    email = models.EmailField(_('email address'), max_length=256, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_deleted = models.BooleanField(_('deleted'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    role = models.CharField(_('role'), max_length=30, blank=False, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['date_joined',]

    def get_full_name(self):
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


class Services(models.Model):
    service_name = models.CharField(max_length=30, null=True)
    service_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)


class UserServices(models.Model):
    service = models.ForeignKey(Services, related_name='service', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='client', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class servicecreate(models.Model):
    first_name = models.CharField(_('first name'), max_length=64, blank=False, null=True)
    last_name = models.CharField(_('last name'), max_length=64, blank=False, null=True)
    email = models.EmailField(_('email address'), max_length=256, unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    
class contact(models.Model):
    first_name = models.CharField(_('first name'), max_length=64, blank=False, null=True)
    last_name = models.CharField(_('last name'), max_length=64, blank=False, null=True)
    email = models.EmailField(_('email address'), max_length=256, unique=True)
    mobile_number = models.IntegerField()
    
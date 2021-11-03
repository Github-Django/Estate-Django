from django.db import models
from django.contrib.auth.models import AbstractUser
from account.myusermanager import MyUserManager


class MyUser(AbstractUser):
    username = None
    mobile = models.CharField(max_length=11, unique=True)
    otp = models.PositiveIntegerField(blank=True, null=True)
    otp_create_time = models.DateTimeField(auto_now=True)
    is_author = models.BooleanField(default=True, verbose_name='نماینده')


    objects = MyUserManager()

    USERNAME_FIELD = 'mobile'

    REQUIRED_FIELDS = []

    backend = 'account.mybackend.ModelBackend'

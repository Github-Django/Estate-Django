import ghasedak
from random import randint
from . import models
import time
from django.utils import timezone
from background_task import background
from .models import MyUser
import requests


@background(schedule=10)
def otp_check_expiration(phone):
    time.sleep(10)
    try:
        user = MyUser.objects.get(phone=phone)
        now = timezone.now()
        otp_time = user.otp_create_time
        diff_time = now - otp_time
        # print(diff_time)

        if diff_time.seconds > 45:
            return False
        return True
    except MyUser.DoesNotExist:
        return False


def get_random_otp():
    return randint(1000, 9999)


def check_otp_expiration(mobile):
    try:
        user = models.MyUser.objects.get(mobile=mobile)
        now = timezone.now()
        otp_time = user.otp_create_time
        diff_time = now - otp_time
        # print('OTP TIME: ', diff_time)

        if diff_time.seconds > 120:
            return False
        return True

    except models.MyUser.DoesNotExist:
        return False


def send_otp(mobile, otp):
    mobile = mobile
    url = "https://api.ghasedak.me/v2/verification/send/simple"
    payload = "receptor={}&template=rafsanjanmelk&type=1&param1={}".format(mobile, otp)
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'apikey': "9f8841933f190d6d88c1c60c2a60ad533856841c8cfeea2c923ea127e54cedab",
        'cache-control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

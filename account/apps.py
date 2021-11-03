from django.apps import AppConfig
from django.core.signals import request_finished
from django.db.models.signals import post_save


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        from . import signals
        from . import models
        request_finished.connect(signals.my_callback)
        post_save.connect(signals.create_new_user, sender=models.MyUser)
        post_save.connect(signals.update_user, sender=models.MyUser)

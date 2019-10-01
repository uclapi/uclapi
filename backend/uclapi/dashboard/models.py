from django.db import models
from .app_helpers import (
    generate_app_id,
    generate_app_client_id,
    generate_app_client_secret,
    generate_secret
)

from common.helpers import generate_api_token

from oauth.models import OAuthScope

from django.db.models.signals import post_save
from django.dispatch import receiver

models.options.DEFAULT_NAMES += ('_DATABASE',)


class User(models.Model):
    email = models.CharField(max_length=100)
    full_name = models.CharField(max_length=1000)
    given_name = models.CharField(max_length=100)
    cn = models.CharField(max_length=100, unique=True)
    department = models.CharField(max_length=1000)
    employee_id = models.CharField(max_length=100, unique=True)
    raw_intranet_groups = models.CharField(max_length=2000)
    agreement = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        _DATABASE = 'default'


class App(models.Model):

    id = models.CharField(
        max_length=20,
        primary_key=True,
        default=generate_app_id
    )
    user = models.ForeignKey(User, related_name='user')
    name = models.CharField(max_length=1000)
    api_token = models.CharField(
        max_length=1000,
        unique=True,
        default=generate_api_token
    )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    deleted = models.BooleanField(default=False)

    client_id = models.CharField(
        max_length=33,
        unique=True,
        default=generate_app_client_id
    )

    client_secret = models.CharField(
        max_length=64,
        unique=True,
        default=generate_app_client_secret
    )

    callback_url = models.CharField(max_length=500, default="")

    def create_scope():
        s = OAuthScope()
        s.save()
        return s.id

    scope = models.ForeignKey(
        OAuthScope,
        on_delete=models.CASCADE,
        default=create_scope)

    def regenerate_token(self):
        new_token = generate_api_token()
        self.api_token = new_token
        self.save()
        return self.api_token

    class Meta:
        _DATABASE = 'default'


class APICall(models.Model):
    ts = models.DateTimeField(auto_now_add=True)
    app = models.ForeignKey(App, related_name='api_call')
    user = models.ForeignKey(User, related_name='api_call')
    raw_request = models.TextField(max_length=10000000)

    class Meta:
        _DATABASE = 'default'


class Webhook(models.Model):
    app = models.OneToOneField(App)
    url = models.URLField(max_length=1000, blank=True)

    siteid = models.CharField(max_length=40, blank=True)
    roomid = models.CharField(max_length=160, blank=True)
    contact = models.CharField(max_length=4000, blank=True)

    last_fired = models.DateTimeField(blank=True, null=True)

    verification_secret = models.CharField(
        max_length=100,
        default=generate_secret
    )

    enabled = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        _DATABASE = 'default'


class WebhookTriggerHistory(models.Model):
    webhook = models.ForeignKey(Webhook)
    payload = models.CharField(max_length=10000000)

    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        _DATABASE = 'default'


# Django signal
@receiver(post_save, sender=App)
def create_webhook_on_app_creation(sender, instance, created, **kwargs):
    if created:
        new_webhook = Webhook(app=instance)
        new_webhook.save()

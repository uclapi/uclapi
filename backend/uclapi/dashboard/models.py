from django.db import models
from .app_helpers import (
    generate_app_id,
    generate_app_client_id,
    generate_app_client_secret,
    generate_secret
)

from common.helpers import generate_api_token

from oauth.models import OAuthScope, OAuthToken

from django.db.models.signals import post_save
from django.dispatch import receiver

models.options.DEFAULT_NAMES += ('_DATABASE',)


class User(models.Model):
    email = models.CharField(max_length=100)
    full_name = models.CharField(max_length=1000)
    given_name = models.CharField(max_length=100)
    sn = models.CharField(max_length=100, default='')
    cn = models.CharField(max_length=100, unique=True)
    department = models.CharField(max_length=1000)
    employee_id = models.CharField(max_length=100, unique=True)
    raw_intranet_groups = models.CharField(max_length=2000)
    user_types = models.CharField(max_length=200, default='')

    # Ideally we'd mandate mail to be unique in the database but as we already have rows in the table, we won't know
    # what value to put in the existing rows during the migration.
    # Note email and mail are very similar... Here's the difference (AFAICT):
    # email: eppn@ucl.ac.uk
    # mail: given_name.sn.$year_of_enrollment@ucl.ac.uk
    mail = models.CharField(max_length=100, default='')
    agreement = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    dev_quota = models.IntegerField(default=10000)
    oauth_quota = models.IntegerField(default=10000)

    class Meta:
        _DATABASE = 'default'


class App(models.Model):

    id = models.CharField(
        max_length=20,
        primary_key=True,
        default=generate_app_id
    )
    user = models.ForeignKey(
        User,
        related_name='user',
        on_delete=models.CASCADE
    )
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
        default=create_scope,
        on_delete=models.CASCADE
    )

    def regenerate_token(self):
        new_token = generate_api_token()
        self.api_token = new_token
        self.save()
        return self.api_token

    class Meta:
        _DATABASE = 'default'


class APICall(models.Model):
    ts = models.DateTimeField(auto_now_add=True)
    app = models.ForeignKey(
        App,
        on_delete=models.CASCADE,
        related_name='api_call'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='api_call'
    )

    token = models.ForeignKey(
        OAuthToken,
        on_delete=models.CASCADE,
        related_name='api_call',
        blank=True,
        null=True
    )
    token_type = models.CharField(max_length=100, default="")
    service = models.CharField(max_length=100, default="")
    method = models.CharField(max_length=100, default="")
    queryparams = models.TextField(max_length=1000, default="")

    class Meta:
        _DATABASE = 'default'


class Webhook(models.Model):
    app = models.OneToOneField(App, on_delete=models.CASCADE)
    url = models.URLField(max_length=1000, blank=True)

    siteid = models.CharField(max_length=40, blank=True)
    roomid = models.CharField(max_length=160, blank=True)
    contact = models.CharField(max_length=4000, blank=True)

    last_fired = models.DateTimeField(blank=True, null=True)
    last_success = models.DateTimeField(blank=True, null=True)

    verification_secret = models.CharField(
        max_length=100,
        default=generate_secret
    )

    enabled = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        _DATABASE = 'default'


class WebhookTriggerHistory(models.Model):
    webhook = models.ForeignKey(
        Webhook,
        on_delete=models.CASCADE
    )
    payload = models.CharField(max_length=10000000)
    status_code = models.IntegerField(null=False)

    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        _DATABASE = 'default'


# Django signal
@receiver(post_save, sender=App)
def create_webhook_on_app_creation(sender, instance, created, **kwargs):
    if created:
        new_webhook = Webhook(app=instance)
        new_webhook.save()

from django.db import models
from .app_helpers import generate_api_token, generate_app_id, generate_app_client_id, generate_app_client_secret
from oauth.models import OAuthScope

models.options.DEFAULT_NAMES += ('_DATABASE',)

# Create your models here.
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

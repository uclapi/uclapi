from django.db import models

from .app_helpers import generate_user_token
from .scoping import Scopes


class OAuthScope(models.Model):
    # We should really have a primary key for the OneToOneField
    id = models.AutoField(primary_key=True)

    # A big integer to store up to 64 types of scope. Avoids lots of boolean comparisons.
    scope_number = models.BigIntegerField(default=0)

    def scopeIsEqual(self, other):
        return self.scope_number == other.scope_number

class OAuthToken(models.Model):
    # Use an incrementing ID that we can always rely on
    # (assume a token could regenerate or be invalidated)
    id = models.AutoField(primary_key=True)
    # The app that requested this token to be created
    app = models.ForeignKey('dashboard.App', on_delete=models.CASCADE)
    # The user that this app will gain access to the data for.
    # Every user that goes through the Shibboleth + OAuth
    # flow will get set up in the default database to ensure that we can fetch
    # their, for example, eppn for custom queries
    user = models.ForeignKey('dashboard.User', on_delete=models.CASCADE)

    # The actual token that can be used by an app to act on behalf of the user
    token = models.CharField(
        max_length=75,
        unique=True,
        default=generate_user_token
    )

    # The scope that the key works within. Every key has a unique scope
    # (in case the developer requests more permissions later)
    scope = models.OneToOneField(
        OAuthScope,
        on_delete=models.CASCADE
    )

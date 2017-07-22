import base64
import hashlib
import hmac
import redis

from django.core.exceptions import ObjectDoesNotExist

from roombookings.helpers import PrettyJsonResponse as JsonResponse
from uclapi.settings import REDIS_UCLAPI_HOST

from .models import OAuthToken
from .scoping import Scopes


def oauth_token_check(required_scopes=None):
    def oauth_token_and_scope(view_func):
        def wrapped(request, *args, **kwargs):
            try:
                client_secret_proof = request.GET['client_secret_proof']
            except KeyError:
                response = JsonResponse({
                    "ok": False,
                    "error": "No Client Secret Proof provided"
                })
                response.status_code = 400
                return response

            try:
                token_code = request.GET["token"]
            except KeyError:
                response = JsonResponse({
                    "ok": False,
                    "error": "No token provided via GET."
                })
                response.status_code = 400
                return response

            try:
                nonce = request.GET["nonce"]
            except KeyError:
                response = JsonResponse({
                    "ok": False,
                    "error": "Nonce not supplied."
                })
                response.status_code = 400
                return response

            r = redis.StrictRedis(host=REDIS_UCLAPI_HOST)
            try:
                nonce_token = r.get(nonce).decode('ascii')
            except:
                response = JsonResponse({
                    "ok": False,
                    "error": "Nonce does not exist."
                })
                response.status_code = 400
                return response

            try:
                token = OAuthToken.objects.get(token=token_code)
            except ObjectDoesNotExist:
                response = JsonResponse({
                    "ok": False,
                    "error": "Token does not exist."
                })
                response.status_code = 400
                return response

            if nonce_token != token_code:
                response = JsonResponse({
                    "ok": False,
                    "error": "Nonce supplied is not for the correct token."
                })
                response.status_code = 400
                return response

            app = token.app
            verification_str = token_code + "&" + nonce
            hmac_digest = hmac.new(bytes(app.client_secret, 'ascii'),
                                   msg=verification_str.encode('ascii'),
                                   digestmod=hashlib.sha256).digest()
            hmac_b64 = base64.b64encode(hmac_digest).decode()
            if client_secret_proof != hmac_b64:
                response = JsonResponse({
                    "ok": False,
                    "error": "Client secret and nonce HMAC verification failed."
                })
                response.status_code = 400
                return response

            scopes = Scopes()
            for s in required_scopes:
                if not scopes.check_scope(token.scope.scope_number, s):
                    response = JsonResponse({
                        "ok": False,
                        "error":
                            "The token provided does not have "
                            "permission to access this data."
                    })
                    response.status_code = 400
                    return response

            kwargs['token'] = token

            return view_func(request, *args, **kwargs)
        return wrapped
    return oauth_token_and_scope

from common.helpers import PrettyJsonResponse as JsonResponse

from .models import OAuthToken
from .scoping import Scopes

# Gets a variable from GET or POST not caring which is which
def get_var(request, var_name):
    if var_name in request.GET:
        return request.GET[var_name]
    elif var_name in request.POST:
        return request.POST[var_name]
    else:
        return None

def oauth_token_check(required_scopes=None):
    def oauth_token_and_scope(view_func):
        def wrapped(request, *args, **kwargs):
            client_secret = get_var(request, 'client_secret')
            if client_secret is None:
                response = JsonResponse({
                    "ok": False,
                    "error": "No Client Secret provided."
                })
                response.status_code = 400
                return response

            token_code = get_var(request, 'token')
            if token_code is None:
                response = JsonResponse({
                    "ok": False,
                    "error": "No token provided via GET."
                })
                response.status_code = 400
                return response

            try:
                token = OAuthToken.objects.get(token=token_code)
            except OAuthToken.DoesNotExist:
                response = JsonResponse({
                    "ok": False,
                    "error": "Token does not exist."
                })
                response.status_code = 400
                return response

            if token.app.client_secret != client_secret:
                response = JsonResponse({
                    "ok": False,
                    "error": "Client secret incorrect."
                })
                response.status_code = 400
                return response

            if not token.active:
                response = JsonResponse({
                    "ok": False,
                    "error":
                        "The token is inactive as the user has revoked "
                        "your app's access to their data."
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

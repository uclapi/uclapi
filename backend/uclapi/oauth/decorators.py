from .models import OAuthToken


def oauth_token_check(scope_name):
    def oauth_token_and_scope(view_func):
        def wrapped(request, *args, **kwargs):
            token = request.GET.get("oauth_token")

            if not token:
                response = JsonResponse({
                    "ok": False,
                    "error": "No Oauth token provided"
                })
                response.status_code = 400
                return response

            try:
                token = OAuthToken.objects.get(api_token=token)
            except ObjectDoesNotExist:
                response = JsonResponse({
                    "ok": False,
                    "error": "Token does not exist"
                })
                response.status_code = 400
                return response

            scope = token.scope

            scope_map = {
                "roombookings": scope.private_roombookings,
                "timetable": scope.private_timetable,
                "uclu": scope.private_uclu
            }

            if not scope_map[scope_name]:
                response = JsonResponse({
                    "ok": False,
                    "error": "No permission to access this data"
                })
                response.status_code = 400
                return response

            return view_func(request, *args, **kwargs)
        return wrapped
    return oauth_token_and_scope

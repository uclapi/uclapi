from dashboard.models import App
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse


def does_token_exist(view_func):
    def wrapped(request, *args, **kwargs):
        token = request.GET.get("token")

        if not token:
            response = JsonResponse({
                "ok": False,
                "error": "No token provided"
            })
            response.status_code = 400
            return response

        try:
            App.objects.get(api_token=token)
        except ObjectDoesNotExist:
            response = JsonResponse({
                "ok": False,
                "error": "Token does not exist"
            })
            response.status_code = 400
            return response

        return view_func(request, *args, **kwargs)
    return wrapped

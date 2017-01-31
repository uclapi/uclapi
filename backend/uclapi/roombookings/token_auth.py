from rest_framework.response import Response
from dashboard.models import App
from django.contrib.auth.models import ObjectDoesNotExist
from django.http import JsonResponse


def does_token_exist(view_func):
    def wrapped(request, *args, **kwargs):
        token = request.GET.get("auth_token")

        if not token:
            return JsonResponse({
                "error": "No token provided"
            })

        try:
            app = App.objects.get(api_token=token)
        except ObjectDoesNotExist:
            return JsonResponse({
                "error": "Token does not exist"
            })

        return view_func(request, *args, **kwargs)
    return wrapped

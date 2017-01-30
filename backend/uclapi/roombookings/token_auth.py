from rest_framework.response import Response
from dashboard.models import App
from django.contrib.auth.models import ObjectDoesNotExist


def does_token_exist(view_func):
    def wrapped(request, *args, **kwargs):
        token = request.GET.get("auth_token")

        if not token:
            return Response({
                "error": "No token provided"
            })

        try:
            app = App.objects.get(api_token=token)
        except DoesNotExist:
            return Response({
                "error": "Token does not exist"
            })

        return view_func(request, *args, **kwargs)
    return wrapped

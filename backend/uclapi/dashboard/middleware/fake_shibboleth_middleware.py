from django.utils.deprecation import MiddlewareMixin


class FakeShibbolethMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        if (
            "convert-post-headers" in request.POST and
            request.POST["convert-post-headers"] == "1"
        ):
            for key in request.POST:
                request.META[key] = request.POST[key]

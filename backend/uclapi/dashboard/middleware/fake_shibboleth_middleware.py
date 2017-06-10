from django.utils.deprecation import MiddlewareMixin


class FakeShibbolethMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        if request.POST.get("convert-post-headers") == "1":
            for key in request.POST:
                request.META[key] = request.POST[key]

        if request.GET.get("convert-get-headers") == "1":
            for key in request.GET:
                http_key = key.upper()
                http_key.replace("-", "_")
                http_key = "HTTP_" + http_key
                request.META[http_key] = request.GET[key]

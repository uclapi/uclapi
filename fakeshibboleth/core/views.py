from django.shortcuts import render

# Create your views here.


def shibboleth(request):
    callback = request.GET["target"]

    context = {
        "callback": callback
    }
    return render(request, "core/shibboleth.html", context)

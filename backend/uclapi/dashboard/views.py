import os
from distutils.util import strtobool

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import quote
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from revproxy.views import ProxyView
from uclapi.settings import FAIR_USE_POLICY
from oauth.app_helpers import (
    get_azure_ad_authorize_url
)

from .app_helpers import get_articles, get_temp_token
from .models import User
from .tasks import add_user_to_mailing_list_task


class DevelopmentNextjsProxyView(ProxyView):
    upstream = 'http://localhost:3000'

@ensure_csrf_cookie
def dashboard(request):
    # Check whether the user is logged in
    try:
        user_id = request.session["user_id"]
    except KeyError:
        # Send the user to AD to log in
        login_url = get_azure_ad_authorize_url(
            request.build_absolute_uri(request.path) + "user/login.callback"
        )
        return redirect(login_url)

    user = User.objects.get(id=user_id)

    if not user.agreement:
        if request.method != "POST":
            return render(request, "agreement.html", {
                'fair_use': FAIR_USE_POLICY
            })

        try:
            agreement = strtobool(request.POST["agreement"])
        except (KeyError, ValueError):
            return render(request, "agreement.html", {
                'fair_use': FAIR_USE_POLICY,
                "error": "You must agree to the fair use policy"
            })

        if agreement:
            user.agreement = True
            user.save()
        else:
            return render(request, "agreement.html", {
                'fair_use': FAIR_USE_POLICY,
                "error": "You must agree to the fair use policy"
            })

    return render(request, 'dashboard.html')

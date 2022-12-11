import os
from distutils.util import strtobool

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import quote
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from uclapi.settings import FAIR_USE_POLICY
from oauth.app_helpers import (
    handle_azure_ad_callback,
    get_azure_ad_authorize_url
)

from .app_helpers import get_articles, get_temp_token
from .models import User
from .tasks import add_user_to_mailing_list_task


@csrf_exempt
def ad_callback(request):
    # Callback from AD login
    # should auth user login or signup
    # then redirect to dashboard homepage
    user_result = handle_azure_ad_callback(
        request.GET.get("code"),
        request.build_absolute_uri(request.path)
    )

    if isinstance(user_result, str):
        response = HttpResponse(
            "Error 400 - Bad Request. <br>" + user_result)
        response.status_code = 400
        return response

    user = user_result

    # TODO update this for AD
    groups = user.raw_intranet_groups
    # Check whether the user is a member of any UCL Intranet Groups.
    # This is a quick litmus test to determine whether they should have
    # access to the dashboard.
    # We deny access to test accounts and alumni, neither of which have
    # this Shibboleth attribute.
    if not groups:
        response = HttpResponse(
            (
                "Error 403 - denied. <br>"
                "The API Dashboard is only accessible to current UCL members."
            )
        )
        response.status_code = 403
        return response

    request.session["user_id"] = user.id
    add_user_to_mailing_list_task.delay(user.email, user.full_name)
    return redirect(dashboard)


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


@ensure_csrf_cookie
def about(request):
    return render(request, 'about.html')


@ensure_csrf_cookie
def home(request):
    logged_in = True

    try:
        request.session["user_id"]
    except KeyError:
        logged_in = False

    articles = get_articles()
    token = get_temp_token()

    return render(request, 'index.html', {
        'initial_data': {
            'temp_token': token,
            'logged_in': str(logged_in),
            'medium_articles': articles
        }
    })


@ensure_csrf_cookie
def documentation(request):
    return render(request, 'documentation.html')


@ensure_csrf_cookie
def warning(request):
    return render(request, 'warning.html')


@ensure_csrf_cookie
def error_404_view(request, exception):
    return render(request, '404.html', status=404)


def error_500_view(request):
    return render(request, '500.html', status=500)


def custom_page_not_found(request):
    return error_404_view(request, None)

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from .models import User
from django.shortcuts import redirect

from django.core.serializers.json import DjangoJSONEncoder
import json


# Create your views here.
def signup(request):
    if request.method == 'POST':
        try:
            eppn = request.META['HTTP_EPPN']
            groups = request.META['HTTP_UCLINTRANETGROUPS']
            cn = request.META['HTTP_CN']
            department = request.META['HTTP_DEPARTMENT']
            given_name = request.META['HTTP_GIVENNAME']
            display_name = request.META['HTTP_DISPLAYNAME']
            employee_id = request.META['EMPLOYEE_ID']
        except KeyError:
            return JsonResponse({
                "error": "Didn't receive any Shibboleth data"
            })

        # create a new user
        new_user = User(
            email=eppn,
            full_name=display_name,
            given_name=given_name,
            department=department,
            cn=cn,
            raw_intranet_groups=groups,
            employee_id=employee_id
        )

        new_user.save()

        # sends the user back to login page
        return redirect('login')


def login(request):
    try:
        eppn = request.META['HTTP_EPPN']
    except KeyError:
        return JsonResponse({
            "error": "Didn't receive any shibboleth data"
        })

    #  get the user and set session for the user
    try:
        user = User.objects.get(email=eppn)
    except:
        return render(request, 'login.html', context={
            "error": "User hasn't registered."
        })

    # set the session for the current logged in user
    reuqest.session["user_id"] = user.id

    # serialise apps and keys

    user_meta = {
        "name": user.given_name,
        "cn": user.cn,
        "department": user.department,
        "intranet_groups": user.raw_intranet_groups,
        "apps": []
    }

    user_apps = Apps.objects.filter(user=user)

    for app in user_apps:
        user_meta["apps"].append({
            "name": app.name,
            "api_token": app.api_token,
            "created": app.created
        })

    return render(request, 'login.html', context=user_meta)

def dashboard(request):
    try:
        user_id = request.session["user_id"]
    except KeyError:
        return render(request, 'login.html')

    user = User.objects.get(id=user_id)

    user_meta = {
        "name": user.given_name,
        "cn": user.cn,
        "department": user.department,
        "intranet_groups": user.raw_intranet_groups,
        "apps": []
    }

    for app in user_apps:
        user_meta["apps"].append({
            "name": app.name,
            "id": app.id,
            "token": app.api_token,
            "created": app.created,
            "updated": app.last_updated
        })

    initial_data = json.dumps(user_meta, cls=DjangoJSONEncoder)
    return render(request, 'dashboard.html', {
	'initial_data': initial_data
    }) 

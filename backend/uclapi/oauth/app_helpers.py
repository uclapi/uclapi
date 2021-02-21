import os
import textwrap
from binascii import hexlify

from django.db.utils import IntegrityError

import dashboard.models
from timetable.models import Lock, StudentsA, StudentsB
from uclapi.settings import SHIB_TEST_USER


def generate_user_token():
    key = hexlify(os.urandom(30)).decode()
    dashes_key = '-'.join(textwrap.wrap(key, 15))
    final = "uclapi-user-" + dashes_key

    return final


def generate_random_verification_code():
    key = hexlify(os.urandom(40)).decode()
    final = "verify" + key
    return final


def get_student_by_upi(upi):
    """Returns a StudentA or StudentB object by UPI"""
    students = StudentsA if Lock.objects.all()[0].a else StudentsB

    # Assume the current Set ID due to caching
    upi_upper = upi.upper()
    student = students.objects.filter(
        qtype2=upi_upper
    )[0]
    return student


def validate_shibboleth_callback(request):
    """Validates user attributes returned from Shibboleth.

    Sometimes UCL doesn't give us the expected headers. If a critical header is
    missing we return a string with the error. If non-critical headers are
    missing we simply put a placeholder string. If all critical headers are
    present we return the User.

    If the user doesn't exist in our database we create a new user. If the user
    already exists, we update fields that are are present in the response.

    :param request: HTTP request.
    :type request: rest_framework.request.Request
    :returns: A valid user derived from the attributes given or an error message.
    :rtype: dashboard.models.User or str
    """
    try:
        # Assumed to be non-empty/unique in many parts of UCL API.
        # i.e. grep -nr '\.email' --include \*.py
        eppn = request.META['HTTP_EPPN']
        # We don't really use cn but because it's unique in the DB we can't
        # really put a place holder value.
        cn = request.META['HTTP_CN']
        # (aka UPI), also unique in the DB
        employee_id = request.META['HTTP_EMPLOYEEID']
    except KeyError:
        return (
            f"UCL has sent incomplete headers. If the issues persist "
            f"please contact the UCL API Team to rectify this. "
            f"The missing fields are (space delimited): "
            f"{'eppn ' if not request.META.get('HTTP_EPPN', None) else ''}"
            f"{'cn ' if not request.META.get('HTTP_CN', None) else ''}"
            f"{'employeeid' if not request.META.get('HTTP_EMPLOYEEID', None) else ''}"
        )

    # TODO: log to sentry that fields were missing...
    department = request.META.get('HTTP_DEPARTMENT', '')
    given_name = request.META.get('HTTP_GIVENNAME', '')
    display_name = request.META.get('HTTP_DISPLAYNAME', '')
    groups = request.META.get('HTTP_UCLINTRANETGROUPS', '')
    mail = request.META.get('HTTP_MAIL', '')
    affiliation = request.META.get('HTTP_AFFILIATION', '')
    unscoped_affiliation = request.META.get('HTTP_UNSCOPED_AFFILIATION', '')
    sn = request.META.get('HTTP_SN', '')

    if not groups and (department == "Shibtests" or eppn == SHIB_TEST_USER):
        groups = "shibtests"

    # If a user has never used the API before then we need to sign them up
    try:
        user = dashboard.models.User.objects.get(employee_id=employee_id)
    except dashboard.models.User.DoesNotExist:
        # create a new user
        try:
            user = dashboard.models.User.objects.create(
                email=eppn, full_name=display_name, given_name=given_name, department=department, cn=cn,
                raw_intranet_groups=groups, employee_id=employee_id, mail=mail, affiliation=affiliation,
                unscoped_affiliation=unscoped_affiliation, sn=sn
            )
        except IntegrityError:
            return (
                "UCL has sent incorrect headers causing an integrity violation. If the issues persist"
                "please contact the UCL API Team to rectify this."
            )
    else:
        # User exists already, so update the values if new ones are non-empty.
        user.email = eppn
        user.cn = cn
        user.full_name = display_name if display_name else user.full_name
        user.given_name = given_name if given_name else user.given_name
        user.department = department if department else user.department
        user.raw_intranet_groups = groups if groups else user.raw_intranet_groups
        user.mail = mail if mail else user.mail
        user.affiliation = affiliation if affiliation else user.affiliation
        user.unscoped_affiliation = unscoped_affiliation if unscoped_affiliation else user.unscoped_affiliation
        user.sn = sn if sn else user.sn
        try:
            user.save()
        except IntegrityError:
            return (
                "UCL has sent incorrect headers causing an integrity violation. If the issues persist"
                "please contact the UCL API Team to rectify this."
            )

    return user

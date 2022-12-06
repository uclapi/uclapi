import os
import textwrap
import logging
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


def validate_azure_ad_callback(token_data):
    """Validates user attributes returned from Azure AD.

    If the user doesn't exist in our database we create a new user. If the user
    already exists, we update fields that are are present in the response.

    :param request: HTTP request.
    :type request: rest_framework.request.Request
    :returns: A valid user derived from the attributes given or an error message.
    :rtype: dashboard.models.User or str
    """

    # To get some of this data, we could decode the JWT, but we need to get at least employee ID which
    # doesn't come in the JWT so we just fetch all the info now
    user_info_result = requests.get(os.environ.get("AZURE_GRAPH_ROOT") +
                                    '/me?$select=department,surname,givenName,displayName,department,userPrincipalName,employeeId,mail,mailNickname&$expand=transitiveMemberOf($select=displayName,mailNickname,classification,description,groupTypes)',
                                    headers={'Authorization': 'Bearer ' + token_data['access_token']})

    if user_info_result.status_code != 200:
        return (
            f"There was an error getting your details from Azure. If the issues persist "
            f"please contact the UCL API Team to rectify this. "
        )

    user_info = user_info_result.json()

    # AD unfortunately restricts $expand to 20 items, so we can't rely on $expand=transitiveMemberOf for the above query. We need to do another one directly for transitiveMemberOf
    # Reference: https://learn.microsoft.com/en-us/graph/known-issues?view=graph-rest-1.0#some-limitations-apply-to-query-parameters
    user_groups_result = requests.get(os.environ.get("AZURE_GRAPH_ROOT") +
                                    '/me/transitiveMemberOf?$select=displayName,mailNickname,classification,description,groupTypes',
                                    headers={'Authorization': 'Bearer ' + token_data['access_token']})

    # TODO: do we really want to treat this as an error?
    if user_groups_result.status_code != 200:
        return (
            f"There was an error getting your details from Azure. If the issues persist "
            f"please contact the UCL API Team to rectify this. "
        )

    # AD groups: displayName.startsWith('+=')
    user_groups = user_groups_result.json()

    # Assumed to be non-empty/unique in many parts of UCL API. i.e. grep -nr '\.email' --include \*.py
    eppn = user_info['userPrincipalName']  # e.g., zxxxxx@ucl.ac.uk
    # We don't really use cn but because it's unique in the DB we can't
    # really put a place holder value.
    cn = user_info['mailNickname']  # e.g., zxxxxx
    # (aka UPI), also unique in the DB
    employee_id = user_info['employeeId']  # e.g., flname12

    department = user_info['department']  # e.g., Dept of Computer Science
    given_name = user_info['givenName']  # e.g. Firstname
    display_name = 'todo full name'
    groups = ';'.join(map(lambda g: g['onPremisesSamAccountName'] or g['mailNickname'], user_groups['value'])) # e.g., engscifac-all;compsci-all;schsci-all
    mail = user_info['mail']  # e.g., firstname.lastname.year@ucl.ac.uk
    affiliation = ''
    unscoped_affiliation = ''
    sn = user_info['surname']

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
                "Microsoft Azure AD has sent incorrect headers causing an integrity violation. If the issues persist"
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
                "Microsoft Azure AD has sent incorrect headers causing an integrity violation. If the issues persist"
                "please contact the UCL API Team to rectify this."
            )

    return user

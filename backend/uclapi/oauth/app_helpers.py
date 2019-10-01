import os
import textwrap
from binascii import hexlify

from timetable.models import Lock, StudentsA, StudentsB


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
    # Returns a StudentA or StudentB object by UPI
    if Lock.objects.all()[0].a:
        students = StudentsA
    else:
        students = StudentsB

    # Assume the current Set ID due to caching
    upi_upper = upi.upper()
    student = students.objects.filter(
        qtype2=upi_upper
    )[0]
    return student

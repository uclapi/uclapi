from django.db import connections
from django.conf import settings
from psycopg2.extras import RealDictCursor

from timetable.amp import ModuleInstance
from timetable.models import Lock

from .utils import (
    get_location_coordinates,
    SESSION_TYPE_MAP
)


def get_personal_timetable_rows(upi):
    set_id = settings.ROOMBOOKINGS_SETID

    # Get from Django's ORM to raw psycopg2 so that a new cursor
    # factory can be used to fetch dicts.

    wrapped_connection = connections['gencache']
    if wrapped_connection.connection is None:
        cursor = wrapped_connection.cursor()

    raw_connection = wrapped_connection.connection

    bucket = 'a' if Lock.objects.all()[0].a else 'b'

    with raw_connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.callproc(
            'get_student_timetable_' + bucket,
            [
                upi,
                set_id
            ]
        )
        rows = cursor.fetchall()
        return rows


def get_personal_timetable(upi):
    full_timetable = {}
    for row in get_personal_timetable_rows(upi):
        instance = ModuleInstance(row['instcode'])
        lat, lng = get_location_coordinates(
            row['siteid'],
            row['roomid']
        )
        if row['lecturereppn'] is None:
            lecturer_email = "Unknown"
        else:
            lecturer_email = "{}@ucl.ac.uk".format(
                row['lecturereppn']
            )
        session_type_str = SESSION_TYPE_MAP[row['sessiontypeid']] \
            if row['sessiontypeid'] in SESSION_TYPE_MAP else "Unknown"

        booking_data = {
            "start_time": row['starttime'],
            "end_time": row['finishtime'],
            "duration": row['duration'],
            "module": {
                "module_id": row['moduleid'],
                "name": row['modulename'],
                "department_id": row['deptid'],
                "department_name": row['deptname'],
                "lecturer": {
                    "name": row['lecturername'],
                    "email": lecturer_email,
                    "department_id": row['lecturerdeptid'],
                    "department_name": row['lecturerdeptname']
                }
            },
            "location": {
                "name": row['roomname'],
                "capacity": row['roomcapacity'],
                "type": row['roomtype'],
                "address": [
                    row['siteaddr1'],
                    row['siteaddr2'],
                    row['siteaddr3'],
                    row['siteaddr4']
                ],
                "site_name": row['sitename'],
                "coordinates": {
                    "lat": lat,
                    "lng": lng
                }
            },
            "session_title": row['title'],
            "session_type": row['sessiontypeid'],
            "session_type_str": session_type_str,
            "session_type_str": row['sessiontypestr'],
            "contact": row['condisplayname'],
            "instance": {
                "delivery": instance.delivery.get_delivery(),
                "periods": instance.periods.get_periods(),
                "instance_code": row['instcode']
            },
            "session_group": row['modgrpcode']
        }

        date = row['startdatetime'].strftime("%Y-%m-%d")
        if date not in full_timetable:
            full_timetable[date] = []
        full_timetable[date].append(booking_data)

    return full_timetable

import gc
import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections

import cx_Oracle
from roombookings.models import BookingA, BookingB, Lock
from django.core.management import call_command

from datetime import datetime
from datetime import timedelta

import pytz

class Command(BaseCommand):

    help = 'Clone Oracle DB to one of the two buckets'

    def handle(self, *args, **options):
        self.stdout.write("Connecting to Oracle...")

        # global connection variable for the database
        con = cx_Oracle.connect(
                user=os.environ.get("DB_ROOMS_USERNAME"),
                password=os.environ.get("DB_ROOMS_PASSWORD"),
                dsn=os.environ.get("DB_ROOMS_NAME")
            )

        cur = con.cursor()

        """
        Our service is only concerned with the current academic year,
        so for 17/18 we would need to ensure the Set ID is LIVE-17-18.
        We generally only offer centrally bookable (CB) rooms but we also
        serve data from the Institute of Child Health (ICH), which has two
        Site IDs:
        238: UCL GOSICH - 30 Guildford Street
        240: UCL GOSICH - Wolfson Centre
        """
        select_query = (
            'SELECT * FROM "CMIS_UCLAPI_V_BOOKINGS"'
            ' WHERE (setid = \'{}\')'.format(settings.ROOMBOOKINGS_SETID)
            + ' AND '
            '(bookabletype = \'CB\' OR siteid = \'238\' OR siteid = \'240\')'
        )

        cur.execute(select_query)

        self.stdout.write("Selecting a clone table...")
        lock = Lock.objects.all()[0]
        current_bucket = BookingA if lock.bookingA else BookingB

        self.stdout.write("Flushing the clone table...")
        # flush the table
        cursor = connections['gencache'].cursor()
        cursor.execute(
            "TRUNCATE TABLE {} RESTART IDENTITY;".format(
                    "roombookings_" + current_bucket.__name__.lower()))

        self.stdout.write(
            "Dumping all the data from Oracle into a new list..."
        )

        batch_size = 5000
        running_total = 0

        while True:
            data_objects = []
            for row in cur.fetchmany(numRows=batch_size):
                data_objects.append(current_bucket(
                    setid=row[0],
                    siteid=row[1],
                    roomid=row[2],
                    sitename=row[3],
                    roomname=row[4],
                    bookabletype=row[5],
                    slotid=row[6],
                    bookingid=row[7],
                    starttime=row[8],
                    finishtime=row[9],
                    startdatetime=row[10],
                    finishdatetime=row[11],
                    weeknumber=row[12],
                    condisplayname=row[13],
                    phone=row[14],
                    descrip=row[15],
                    title=row[16]
                ))

            data_objects_size = len(data_objects)

            # If there's no more data, quit
            if data_objects_size == 0:
                break

            self.stdout.write("Inserting records {} => {}".format(
                running_total + 1,
                running_total + data_objects_size)
            )
            current_bucket.objects.using("gencache").bulk_create(
                data_objects
            )
            running_total += data_objects_size
            data_objects.clear()

            gc.collect()

        self.stdout.write("Inserted {} records.".format(running_total))

        self.stdout.write("Updating the lock...")
        lock.bookingA = not lock.bookingA
        lock.bookingB = not lock.bookingB
        lock.save()

        self.stdout.write("Updated a bucket!")

        wr = open("time.txt", 'w')
        cache_expires = datetime.now(pytz.utc)+timedelta(minutes=20)
        # Convert and write HTTP date format
        wr.write(cache_expires.strftime("%a, %d %b %Y %X %Z"))
        wr.close()

        gc.collect()
        call_command('trigger_webhooks')

import os

from django.core.management.base import BaseCommand
from django.conf import settings

import cx_Oracle
from roombookings.models import BookingA, BookingB, Lock


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

        select_query = (
            'SELECT * FROM "CMIS_UCLAPI_V_BOOKINGS"'
            ' WHERE (bookabletype = \'CB\' AND setid'
            ' = \'{}\')'.format(settings.ROOMBOOKINGS_SETID)
        )

        cur.execute(select_query)

        self.stdout.write("Selecting a clone table...")
        lock = Lock.objects.all()[0]
        curr = BookingA if lock.bookingA else BookingB

        self.stdout.write("Flushing the clone table...")
        # flush the table
        curr.objects.using("gencache").all().delete()

        self.stdout.write(
            "Dumping all the data from Oracle into a new list..."
        )
        data_objects = []

        for row in cur:
            data_objects.append(curr(
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

        self.stdout.write("There are " + str(len(data_objects)) + " records.")

        self.stdout.write("Bulk creating this in PostgreSQL...")
        curr.objects.using("gencache").bulk_create(
            data_objects,
            batch_size=5000
        )

        self.stdout.write("Updating the lock...")
        lock.bookingA = not lock.bookingA
        lock.bookingB = not lock.bookingB
        lock.save()

        self.stdout.write("Updated a bucket!")

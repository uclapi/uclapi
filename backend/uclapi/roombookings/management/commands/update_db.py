import os
import cx_Oracle
import datetime
from roombookings.models import BookingA, BookingB, Lock
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'clone oracle db to one of the two buckets'

    def handle(self, *args, **options):
        # global connection variable for the database
        con = cx_Oracle.connect(
                user=os.environ.get("DB_ROOMS_USERNAME"),
                password=os.environ.get("DB_ROOMS_PASSWORD"),
                dsn=os.environ.get("DB_ROOMS_NAME")
            )

        cur = con.cursor()

        select_query = ('SELECT * FROM "CMIS_UCLAPI_V_BOOKINGS"'
                        ' WHERE (bookabletype = \'CB\' AND setid'
                        ' = \'LIVE-16-17\')'
                        )

        cur.execute(select_query)

        lock = Lock.objects.all()[0]
        curr = BookingA if lock.bookingA else BookingB

        # flush the table
        curr.objects.all().delete()

        for row in cur:
            bk = curr(
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
                descrip=row[15]
            )
            bk.save()

        lock.bookingA = not lock.bookingA
        lock.bookingB = not lock.bookingB
        lock.save()

        self.stdout.write("updated one of the bucket")

from django.core.management.base import BaseCommand
from roombookings.models import Lock, BookingA, BookingB
from roombookings.helpers import _serialize_bookings
from dashboard.models import WebHook
from datetime import datetime
from deepdiff import DeepDiff
import grequests
from django.utils import timezone


class Command(BaseCommand):

    help = 'Diff roombooking result sets and notify relevant webhooks'

    def handle(self, *args, **options):
        self.stdout.write("Triggering webhooks")

        # currently locked table is the old one, more recent one is not locked
        lock = Lock.objects.all()[0]  # there is only ever one lock

        if lock.bookingA:
            old_booking_table = BookingA
            new_booking_table = BookingB
        else:
            old_booking_table = BookingB
            new_booking_table = BookingA

        now = datetime.now()

        old_bookings = _serialize_bookings(
            old_booking_table.objects.filter(
                startdatetime__gt=now
            )
        )
        new_bookings = _serialize_bookings(
            new_booking_table.objects.filter(
                startdatetime__gt=now
            )
        )

        ddiff = DeepDiff(old_bookings, new_bookings, ignore_order=True)
        bookings_added = ddiff["iterable_item_added"].values()
        bookings_removed = ddiff["iterable_item_removed"].values()

        webhooks = WebHook.objects.all()
        #  assumption: list of webhooks will be longer than ddiff

        def webhook_map(webhook):
            def webhook_filter(booking):
                return (
                    (
                        webhook.siteid == '' or
                        booking["siteid"] == webhook.siteid
                    ) and
                    (
                        webhook.roomid == '' or
                        booking["roomid"] == webhook.roomid
                    ) and
                    (
                        webhook.contact == '' or
                        # mimick SQL 'like'
                        webhook.contact in booking["contact"]
                    )
                )
            return {
                "webhook_in_db": webhook,
                "url": webhook.url,
                "bookings_added": list(filter(webhook_filter, bookings_added)),
                "bookings_removed": list(
                    filter(webhook_filter, bookings_removed)
                ),
            }

        webhooks_to_enact = list(map(webhook_map, webhooks))

        unsent_requests = [grequests.post(
            webhook["url"], json={
                "bookings_added": webhook["bookings_added"],
                "bookings_removed": webhook["bookings_removed"],
            }
        ) for webhook in webhooks_to_enact]
        grequests.map(unsent_requests)

        for webhook in webhooks_to_enact:
            webhook_in_db = webhook["webhook_in_db"]
            webhook_in_db.last_fired = timezone.now()
            webhook_in_db.save()

        self.stdout.write("Webhooks triggered.")

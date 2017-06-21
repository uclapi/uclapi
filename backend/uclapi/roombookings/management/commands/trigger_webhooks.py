from django.core.management.base import BaseCommand
from roombookings.models import Lock, BookingA, BookingB
from roombookings.helpers import _serialize_bookings
from dashboard.models import Webhook, WebhookTriggerHistory
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

        webhooks = Webhook.objects.all()
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
            output = {
                "webhook_in_db": webhook,
                "url": webhook.url
            }
            if "iterable_item_added" in ddiff:
                output["bookings_added"] = list(filter(
                    webhook_filter, ddiff["iterable_item_added"].values()
                ))
            if "iterable_item_removed" in ddiff:
                output["bookings_removed"] = list(filter(
                    webhook_filter, ddiff["iterable_item_removed"].values()
                ))

            return output

        webhooks_to_enact = list(map(webhook_map, webhooks))

        unsent_requests = []
        for idx, webhook in enumerate(webhooks_to_enact):
            payload = {}

            if "bookings_added" in webhook:
                payload["bookings_added"] = webhook["bookings_added"]
            if "bookings_removed" in webhook:
                payload["bookings_removed"] = webhook["bookings_removed"]

            webhooks_to_enact[idx]["payload"] = payload

            if payload != {}:
                unsent_requests.append(
                    grequests.post(
                        webhook["url"], json=payload, headers={
                            "User-Agent": "uclapi-bot/1.0"
                        }
                    )
                )
        grequests.map(unsent_requests)

        for webhook in webhooks_to_enact:
            if webhook["payload"] != {}:
                webhook_in_db = webhook["webhook_in_db"]
                webhook_in_db.last_fired = timezone.now()
                webhook_in_db.save()

                new_webhook_history_entry = WebhookTriggerHistory(
                    webhook=webhook_in_db,
                    payload=webhook["payload"]
                )
                new_webhook_history_entry.save()

        self.stdout.write("Webhooks triggered.")

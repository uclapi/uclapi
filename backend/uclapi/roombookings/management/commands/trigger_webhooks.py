from django.core.management.base import BaseCommand
from roombookings.models import BookingA, BookingB
from timetable.models import Lock
from roombookings.helpers import _serialize_bookings
from dashboard.models import Webhook, WebhookTriggerHistory
from datetime import datetime
from deepdiff import DeepDiff
from django.utils import timezone
from requests_futures.sessions import FuturesSession
from django.db.models import Q


class Command(BaseCommand):

    help = 'Diff roombooking result sets and notify relevant webhooks'

    def add_arguments(self, parser):
        parser.add_argument(
            '--debug',
            action='store_true',
            dest='debug',
            help='Print webhook responses',
        )

    def handle(self, *args, **options):
        self.stdout.write("Triggering webhooks")
        session = FuturesSession()

        # currently not locked table is the old one, more recent one is locked
        lock = Lock.objects.all()[0]  # there is only ever one lock

        if not lock.a:
            old_booking_table = BookingA
            new_booking_table = BookingB
        else:
            old_booking_table = BookingB
            new_booking_table = BookingA

        now = datetime.now()

        old_bookings = _serialize_bookings(
            old_booking_table.objects.filter(
                Q(bookabletype='CB') | Q(siteid='238') | Q(siteid='240'),
                startdatetime__gt=now
            )
        )
        new_bookings = _serialize_bookings(
            new_booking_table.objects.filter(
                Q(bookabletype='CB') | Q(siteid='238') | Q(siteid='240'),
                startdatetime__gt=now
            )
        )

        ddiff = DeepDiff(old_bookings, new_bookings, ignore_order=True)

        webhooks = Webhook.objects.filter(app__deleted=False)
        #  assumption: list of webhooks will be longer than ddiff

        num_bookings_added = 0
        num_bookings_removed = 0
        if "iterable_item_added" in ddiff:
                num_bookings_added = len(
                    ddiff["iterable_item_added"].values()
                )

        if "iterable_item_removed" in ddiff:
                num_bookings_removed = len(
                    ddiff["iterable_item_removed"].values()
                )

        self.stdout.write(
            "{} bookings added\n{} bookings removed.".format(
                num_bookings_added,
                num_bookings_removed
            )
        )

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
                        webhook.contact in str(booking["contact"])
                    )
                )
            output = {
                "webhook_in_db": webhook,
                "url": webhook.url,
                "verification_secret": webhook.verification_secret
            }
            if "iterable_item_added" in ddiff:
                bookings_added = list(filter(
                    webhook_filter, ddiff["iterable_item_added"].values()
                ))
                if bookings_added != []:
                    output["bookings_added"] = bookings_added
            if "iterable_item_removed" in ddiff:
                bookings_removed = list(filter(
                    webhook_filter, ddiff["iterable_item_removed"].values()
                ))
                if bookings_removed != []:
                    output["bookings_removed"] = bookings_removed

            return output

        webhooks_to_enact = list(map(webhook_map, webhooks))

        unsent_requests = []
        for idx, webhook in enumerate(webhooks_to_enact):
            payload = {
                "service": "roombookings",
                "name": "bookings_changed",
                "verification_secret": webhook["verification_secret"],
                "content": {}
            }

            if "bookings_added" in webhook:
                payload["content"]["bookings_added"] = (
                    webhook["bookings_added"]
                )
            if "bookings_removed" in webhook:
                payload["content"]["bookings_removed"] = (
                    webhook["bookings_removed"]
                )

            webhooks_to_enact[idx]["payload"] = payload

            if payload["content"] != {} and webhook["url"] != "":
                unsent_requests.append(
                    session.post(
                        webhook["url"], json=payload,
                        headers={
                            "User-Agent": "uclapi-bot/1"
                        }
                    )
                )
        self.stdout.write(
            "Triggering {} webhooks.".format(len(unsent_requests))
        )
        if("debug" in options):
            for i in unsent_requests:
                self.stdout.write(
                    'response status {0}'.format(i.result().status_code)
                )

        for webhook in webhooks_to_enact:
            if webhook["payload"]["content"] != {}:
                webhook_in_db = webhook["webhook_in_db"]
                webhook_in_db.last_fired = timezone.now()
                webhook_in_db.save()

                new_webhook_history_entry = WebhookTriggerHistory(
                    webhook=webhook_in_db,
                    payload=webhook["payload"]
                )
                new_webhook_history_entry.save()

        self.stdout.write("Webhooks triggered.")

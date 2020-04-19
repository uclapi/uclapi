from django.core.management.base import BaseCommand

from dashboard.models import User, App, APICall, Webhook, WebhookTriggerHistory


class Command(BaseCommand):

    help = 'Cleans Dashboard of everything'

    def handle(self, *args, **options):
        string = input("THIS WILL WIPE THESE MODELS ARE YOU SURE? "
                       "TYPE DELETE TO CONFIRM!: ")
        if string == "DELETE":
            User.objects.all().delete()
            App.objects.all().delete()
            APICall.objects.all().delete()
            Webhook.objects.all().delete()
            WebhookTriggerHistory.objects.all().delete()

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

from dashboard.models import App, User
from timetable.models import Lock as TimetableLock


class Command(BaseCommand):
    help = 'Sets up the development environment for Docker'

    def handle(self, *args, **options):
        if not settings.DEBUG:
            print("This must not be run in production!")
            return

        print("Setting up the well-known development user...")
        try:
            # The email is set from the EPPN header
            user = User.objects.get(email='develop@ucl.ac.uk')
        except User.DoesNotExist:
            user = User(
                email='develop@ucl.ac.uk',
                full_name='UCL API Developer',
                given_name='UCL API',
                department='Dept of API Development',
                cn='develop',
                raw_intranet_groups='ucl-all;ucl-ug;schsci-all',
                employee_id='uclapi1'
            )
            user.save()

        print("Setting up the well-known Local OAuth Test app...")
        try:
            app = App.objects.get(user=user, name="Local OAuth Test")
        except App.DoesNotExist:
            app = App(
                user=user,
                name="Local OAuth Test",
                api_token='uclapi-4286bc18b235d86-ab0998cc3a47a9b-07b6dfe234a04bf-97407a655b33ae8',  # noqa
                client_id='1105308584328350.9460393713696551',
                client_secret='251e9f9553bb3b86829c18bf795844d977dedf569b24a70e4d4e753958fcc2f3',    # noqa
                callback_url='http://localhost:8002/uclapi/callback'
            )
            app.save()

        print(
            "Well-known user: {}. Well-known app: {}".format(
                user.full_name,
                app.name
            )
        )

        if len(TimetableLock.objects.all()) == 0:
            call_command("create_timetable_lock")

        print("Building Medium Cache...")
        call_command("update_medium")

        print("*** Development environment ready for use! ***")

from django.core.management.base import BaseCommand
from roombookings.models import RoomCache


class Command(BaseCommand):

    help = 'Clone room data to gencache'

    def handle(self, *args, **options):
        with open('roombookings/management/commands/data/rooms.csv') as f:
            room_data = f.read()

        room_data = room_data.split('\n')

        room_data = list(map(lambda k: k.split(','), room_data))
        self.stdout.write("Delete existing table")
        RoomCache.objects.all().delete()
        for room in room_data[1:]:
            try:
                room_cache = RoomCache(
                    setid=room[0],
                    siteid=room[1],
                    sitename=room[2],
                    address1=room[3],
                    address2=room[4],
                    address3=room[5],
                    addres4=room[6],
                    roomid=room[7],
                    roomname=room[8],
                    roomdeptid=room[9],
                    bookabletype=room[10],
                    roomclass=room[11],
                    zone=room[12],
                    webview=room[13],
                    automated=room[14],
                    capacity=room[15],
                    category=room[16]
                )
                room_cache.save()
            except IndexError:
                # last or first line?
                pass
        self.stdout.write("Done and dusted")

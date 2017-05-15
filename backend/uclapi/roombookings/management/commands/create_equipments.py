from django.core.management.base import BaseCommand
from roombookings.models import EquipmentCache


class Command(BaseCommand):

    help = 'Equipment data for gencache'

    def handle(self, *args, **options):
        with open('roombookings/management/commands/data/equipment.csv') as f:
            equip_data = f.read()

        equip_data = equip_data.split('\n')

        equip_data = list(map(lambda k: k.split(','), equip_data))

        for eq in equip_data[1:]:
            try:
                equip_cache = EquipmentCache(
                    setid=eq[0],
                    roomid=eq[1],
                    units=eq[2],
                    description=eq[3],
                    siteid=eq[4],
                    type=eq[5]
                )
                equip_cache.save()
            except IndexError:
                # last or first line?
                pass
        self.stdout.write("Done and dusted")

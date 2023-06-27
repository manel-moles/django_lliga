from lliga.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Esborra tots els registres de la base de dades'

    def handle(self, *args, **options):
        records = Event.objects.all()
        records.delete()
        records = Partit.objects.all()
        records.delete()
        records = Jugador.objects.all()
        records.delete()
        records = Equip.objects.all()
        records.delete()
        records = Lliga.objects.all()
        records.delete()
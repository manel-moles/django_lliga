from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker
from datetime import timedelta, time
from random import randint
 
from lliga.models import *
 
faker = Faker(["es_CA","es_ES"])
 
class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'
 
    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)
 
    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]
        lliga = Lliga.objects.filter(titol=titol_lliga)
        if lliga.count()>0:
            print("Aquesta lliga ja està creada. Posa un altre nom.")
            return
 
        print("Creem la nova lliga: {}".format(titol_lliga))
        lliga = Lliga(  titol=titol_lliga)
        lliga.save()
 
        print("Creem equips")
        prefixos = ["RCD", "Athletic", "", "Deportivo", "Sporting"]
        for i in range(20):
            ciutat = faker.city()
            prefix = prefixos[randint(0,len(prefixos)-1)]
            if prefix:
                prefix += " "
            nom =  prefix + ciutat
            any_fundacio  = faker.random_int(min=1890, max=1990)
            equip = Equip(ciutat=ciutat,equip=nom,any_fundacio=any_fundacio)
            #print(equip)
            equip.save()
            lliga.equips.add(equip)
 
            print("Creem jugadors de l'equip "+nom)
            for j in range(25):
                nom = faker.first_name()
                cognom1 = faker.last_name()
                cognom2 = faker.last_name()
                jugador = Jugador(nom=nom + " " + cognom1 + " " + cognom2,equip=equip,alias=nom,dorsal=j+1)
                #print(jugador)
                jugador.save()
 
        print("Creem partits de la lliga")
        for local in lliga.equips.all():
            for visitant in lliga.equips.all():
                if local!=visitant:
                    print("Generant partit " + str(local) + " vs " + str(visitant))
                    partit = Partit(local=local,visitant=visitant)
                    partit.local = local
                    partit.visitant = visitant
                    partit.lliga = lliga
                    partit.save()
                    for n in range(faker.random_int(min=0, max=6)):
                        tipus=Event.EventType.GOL
                        temps=time(0,randint(0,45),randint(0,59))
                        part=randint(1,2)
                        if(randint(0,1)):
                            equip=local
                        else:
                            equip=visitant
                        jugador=equip.jugador_set.all()[randint(0,20)]
                        event = Event(partit=partit,tipus=tipus, temps = temps, part=part,equip=equip, jugador=jugador)
                        event.save()

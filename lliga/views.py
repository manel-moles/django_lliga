from django.shortcuts import render
from django.http import HttpResponse

from .models import *


def index(request):
    return HttpResponse("Hello, world. You're at the lliga index.")

def classificacio(request):
    lliga = Lliga.objects.first()
    equips = lliga.equips.all()
    classi = []
 
    # calculem punts en llista de tuples (equip,punts)
    for equip in equips:
        punts = 0
        for partit in lliga.partit_set.filter(local=equip):
            if partit.gols_local() > partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        for partit in lliga.partit_set.filter(visitant=equip):
            if partit.gols_local() < partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        classi.append( (punts,equip.equip) )
    # ordenem llista
    classi.sort(reverse=True)
    return render(request,"lliga/classificacio.html",
                {
                    "classificacio":classi,
                })


def taula_partits(request):
    lliga = Lliga.objects.first()
    equips = lliga.equips.all()
    taula = []
 
    # calculem punts en llista de tuples (equip,punts)
    for local in equips:
        fila = []
        fila.append(str(local))
        for visitant in equips:
            if(local!=visitant):
                partits = lliga.partit_set.filter(local=local, visitant=visitant)
                partit=partits.first()
                fila.append( str(partit.gols_local()) + " - " + str(partit.gols_visitant()))
            else:
                fila.append( "X")
 
        taula.append( fila )

    return render(request,"lliga/taula_partits.html",
                {
                    "taula_partits":taula,
                })
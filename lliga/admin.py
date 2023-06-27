from django.contrib import admin

# Register your models here.
from .models import Lliga, Equip, Jugador, Partit, Event

class LligaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["lliga", "temporada"]})
    ]

admin.site.register(Lliga,LligaAdmin)

class JugadorInline(admin.TabularInline):
    model = Jugador
    extra = 0
class EquipAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["equip","any_fundacio","lliga"]})
    ]
    inlines = [JugadorInline]

admin.site.register(Equip,EquipAdmin)

admin.site.register(Jugador)

class EventInline(admin.TabularInline):
    model = Event
    fields = ["temps","tipus","jugador","equip"]
    ordering = ("temps",)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # filtrem els jugadors i només deixem els que siguin d'algun dels 2 equips (local o visitant)
        if db_field.name == "jugador":
            partit_id = request.resolver_match.kwargs['object_id']
            partit = Partit.objects.get(id=partit_id)
            jugadors_local = [jugador.id for jugador in partit.local.jugador_set.all()]
            jugadors_visitant = [jugador.id for jugador in partit.visitant.jugador_set.all()]
            jugadors = jugadors_local + jugadors_visitant
            kwargs["queryset"] = Jugador.objects.filter(id__in=jugadors)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)            

class PartitAdmin(admin.ModelAdmin):
        # podem fer cerques en els models relacionats
        # (noms dels equips o títol de la lliga)
	search_fields = ["local__nom","visitant__nom","lliga__titol"]
        # el camp personalitzat ("resultats" o recompte de gols)
        # el mostrem com a "readonly_field"
	readonly_fields = ["resultat",]
	list_display = ["local","visitant","resultat","lliga","inici"]
	ordering = ("-inici",)
	inlines = [EventInline,]
	def resultat(self,obj):
		gols_local = obj.event_set.filter(
		                tipus=Event.EventType.GOL,
                                equip=obj.local).count()
		gols_visit = obj.event_set.filter(
		                tipus=Event.EventType.GOL,
                                equip=obj.visitant).count()
		return "{} - {}".format(gols_local,gols_visit)

admin.site.register(Partit,PartitAdmin)
admin.site.register(Event)



from django.urls import path
from . import views

app_name ="lliga"
urlpatterns = [
    path("",views.index, name="index"),
    path("classificacio",views.classificacio, name="classificacio"),
    path("taula_partits",views.taula_partits, name="taula_partits"),
]
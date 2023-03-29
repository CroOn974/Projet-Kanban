from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ColonneViewset, TacheViewset

colonne = DefaultRouter()
colonne.register('colonne', ColonneViewset, basename= 'colonne')

tache = DefaultRouter()
tache.register('tache', TacheViewset, 'tache')

urlpatterns = [
    path('', include(colonne.urls)),
    path('', include(tache.urls)),

]
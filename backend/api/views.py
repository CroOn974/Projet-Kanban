from django.shortcuts import render
from api.models import Colonne, Tache
from api.serializers import ColonneSerializer, TacheSerializer, SwitchColonneSerializer
from django.db.models import F
#API
from rest_framework.response import Response
from rest_framework import viewsets


##
# CRUD Colonne
# EndPoint -> http://localhost:8000/api/colonne/
#
class ColonneViewset(viewsets.ModelViewSet):
    queryset = Colonne.objects.all().order_by('position_colonne')
    serializer_class = ColonneSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        nbColonnes = Colonne.objects.filter(position_colonne__isnull=False).count()
        instance.position_colonne = nbColonnes
        instance.save()
    
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        # récupère la colonne et la position de la tache avant update
        queryset = Colonne.objects.get(id_colonne = instance.id_colonne)
        position = queryset.position_colonne

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # récupère la position après update
        newPosition = serializer.validated_data['position_colonne']

        queryset = Colonne.objects.all()
        print(newPosition)
        print(position)
        
        if newPosition > position:
            print('sup')

            # recupère toutes le tache entre l'ancien position et la nouvelle
            # lt >
            # lte >=
            # gt <
            # gte <=
            queryset = queryset.filter(position_colonne__gte=position,
                                     position_colonne__lte=newPosition)
            
            queryset.update(position_colonne=F('position_colonne') - 1)
            Colonne.objects.filter(id_colonne=instance.id_colonne).update(position_colonne=F('position_colonne') + 1)

        elif newPosition < position:
            print('inf')
            queryset = queryset.filter(position_colonne__gte=newPosition, position_colonne__lte=position)
            
            for obj in queryset:
                print(obj)
            queryset.update(position_colonne=F('position_colonne') + 1)
            Colonne.objects.filter(id_colonne=instance.id_colonne).update(position_colonne=F('position_colonne') - 1)

        return super().update(request, *args, **kwargs)


##
# CRUD Tache
# EndPoint -> http://localhost:8000/api/tache/
#
class TacheViewset(viewsets.ModelViewSet):
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        nbColonne = instance.id_colonne
        nbTache = Tache.objects.filter(id_colonne = nbColonne).count()
        instance.position_tache = nbTache
        instance.save()
      
        return Response(serializer.data)

    # Update Tache
    def partial_update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        # récupère la colonne et la position de la tache avant update
        queryset = Tache.objects.get(id_tache = instance.id_tache)
        colonne = queryset.id_colonne
        position = queryset.position_tache

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # récupère la colone et la position après update
        newColonne = serializer.validated_data['id_colonne']
        newPosition = serializer.validated_data['position_tache']

        queryset = Tache.objects.filter(id_colonne=newColonne)

        # verifie si la tache a changer de colonne
        if colonne == newColonne:
            if newPosition > position:
                # recupère toutes le tache entre l'ancien position et la nouvelle
                queryset = queryset.filter(position_tache__lt=newPosition,position_tache__gt=position)
                
                queryset.update(position_tache=F('position_tache') - 1)
                Tache.objects.filter(id_tache=instance.id_tache).update(position_tache=F('position_tache') - 1)

            elif newPosition < position:
                # recupère toutes le tache entre l'ancien position et la nouvelle
                queryset = queryset.filter(position_tache__lte=position,
                                            position_tache__gte=newPosition)

                queryset.update(position_tache=F('position_tache') + 1)
                Tache.objects.filter(id_tache=instance.id_tache).update(position_tache=F('position_tache') - 1)

        else: # nouvelle colonne

            # récupération des tâches qui doivent être mises à jour
            queryset = queryset.filter(position_tache__gte= newPosition).exclude(id_tache=instance.id_tache)
            # mise à jour de la position des tâches
            queryset.update(position_tache=F('position_tache') + 1)


            # mise a jour de l'ancien colonne
            # récupération des tâches qui doivent être mises à jour
            queryset = Tache.objects.filter(id_colonne=colonne)
            queryset = queryset.filter(position_tache__gte= position)
            # mise à jour de la position des tâches
            queryset.update(position_tache=F('position_tache') - 1)


        return Response(serializer.data)

    # Delete Tache
    def perform_destroy(self, instance):
        # récupérer la position de la tâche à supprimer
        position = instance.position_tache
        # supprimer la tâche
        instance.delete()
        # décrémenter la position des tâches suivantes
        Tache.objects.filter(position_tache__gt=position).update(position_tache=F('position_tache') - 1)
    
        

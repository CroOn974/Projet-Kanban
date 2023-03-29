from django.shortcuts import render
from api.models import Colonne, Tache
from api.serializers import ColonneSerializer, TacheSerializer
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
        instance.position_tache = nbTache - 1
        instance.save()
      
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        print(instance.id_tache)
        lastPosition = Tache.objects.get(id_tache = instance.id_tache)
        print('last')
        print(lastPosition.id_colonne)

        # Update the instance with the new data
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Get the new position of the task
        id_colonne = serializer.validated_data['id_colonne']
        new_position = serializer.validated_data['position_tache']
        queryset = Tache.objects.filter(id_colonne=id_colonne)

        print('new')
        print(id_colonne)
        


        # Adjust the position of other tasks in the column
        if new_position > instance.position_tache:
            # Moving the task downwards
            print("sp")
            queryset = queryset.filter(position_tache__gt=instance.position_tache,
                                    position_tache__lte=new_position)
            print(queryset)
            queryset.update(position_tache=F('position_tache') - 1)
        elif new_position < instance.position_tache:
            # Moving the task upwards
            print("inf")
            queryset = queryset.filter(position_tache__gte=new_position,
                                    position_tache__lt=instance.position_tache)
            print(queryset)
            queryset.update(position_tache=F('position_tache') + 1)

        return Response(serializer.data)


        

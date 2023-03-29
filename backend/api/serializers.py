from rest_framework import serializers
from api.models import Colonne, Tache

class ColonneSerializer(serializers.ModelSerializer):
    tache = serializers.SerializerMethodField()

    class Meta:
        model = Colonne
        fields = ('id_colonne','titre_colonne', 'position_colonne', 'tache')

    def get_tache(self, obj):
        return [{'id_tache': tache.id_tache, 'titre_tache': tache.titre_tache, 'position_tache': tache.position_tache} for tache in obj.tache_set.all().order_by('position_tache')]
    

class TacheSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tache
        fields = '__all__'
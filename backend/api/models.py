from django.db import models


class Colonne(models.Model):
    id_colonne = models.AutoField(primary_key=True)
    titre_colonne = models.CharField(max_length=50)
    position_colonne = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'colonne'


class Tache(models.Model):
    id_tache = models.AutoField(primary_key=True)
    titre_tache = models.CharField(max_length=50)
    position_tache = models.IntegerField()
    id_colonne = models.ForeignKey(Colonne, on_delete=models.CASCADE, db_column='id_colonne')

    class Meta:
        managed = False
        db_table = 'tache'
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.fields import ArrayField

from users.models import User


class CategoriaSintoma(models.Model):
    identificador = models.CharField(max_length=255)
    pregunta = models.CharField(max_length=255)

    def __str__(self):
        return self.pregunta


class Sintoma(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(blank=True, max_length=255)
    categoria = models.ForeignKey('CategoriaSintoma', null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Síntoma historial'
        verbose_name_plural = 'Síntomas historiales'


class Historial(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    sintomas = models.ManyToManyField('Sintoma', blank=True)

    def __str__(self):
        return str(self.usuario)


class TipoRespuesta(models.Model):
    identificador = models.CharField(max_length=255, unique=True)
    opciones = ArrayField(models.CharField(max_length=25,))

    def __str__(self):
        return self.identificador


class Pregunta(models.Model):
    pregunta = models.CharField(max_length=255)
    tipo_respuesta = models.ForeignKey('TipoRespuesta', null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.pregunta


class EntradaDiario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    fecha = models.DateField(null=True, default=None)
    coordenadas = gis_models.PointField(null=True, default=None, blank=True)
    preguntas = models.ManyToManyField('Pregunta', through='ValorRespuesta')
    comentario = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return str(self.fecha)


class ValorRespuesta(models.Model):
    entrada_diario = models.ForeignKey(EntradaDiario, on_delete=models.DO_NOTHING)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.DO_NOTHING)
    respuesta = models.CharField(blank=True, max_length=25)

    def __str__(self):
        return self.respuesta

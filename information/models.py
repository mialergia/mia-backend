from django.db import models


class TerminosCondiciones(models.Model):
    texto = models.CharField(max_length=10000)

    def __str__(self):
        return self.texto


class Notificacion(models.Model):
    texto = models.CharField(max_length=255)

    def __str__(self):
        return self.texto

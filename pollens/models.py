from django.db import models
import django.utils.timezone
import math
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

from information.send_push_notification import send_push_notification
from users.models import User
from alergias.strings import critical_reports
import unicodedata


class GrupoPolinico(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    nombre = models.CharField(max_length=50)
    unidad_medida = models.CharField(max_length=12)
    nivel_alto = models.IntegerField(default=1)
    nivel_medio = models.IntegerField(default=1)
    nivel_alto_sumatoria = models.IntegerField(blank=True, null=True)
    nivel_medio_sumatoria = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Polen(models.Model):
    tipo = models.CharField(blank=True, max_length=50)
    nombre_cientifico = models.CharField(blank=True, max_length=50)
    nombre_comun = models.CharField(max_length=50)
    familia = models.CharField(blank=True, max_length=50)
    picks_presente = models.BooleanField(blank=True)
    grupo_polinico = models.ForeignKey(GrupoPolinico, related_name="polenes", on_delete=models.CASCADE)
    alergenicidad = models.CharField(blank=True, max_length=50)
    nivel_alto = models.FloatField()
    nivel_medio = models.FloatField()
    nombre_alergia = models.CharField(blank=True, max_length=50, default="")
    archivo_pdf = models.FileField(blank=True, upload_to='pdfs/', null=True)

    @property
    def archivo_pdf_url(self):
        if self.archivo_pdf and hasattr(self.archivo_pdf, 'url'):
            return self.archivo_pdf.url

    def get_name_file(self):
        file_name = self.archivo_pdf.name
        if (file_name is None or file_name == ''):
            return None
        name, extension = os.path.splitext(file_name)
        nfkd_form = unicodedata.normalize('NFKD', self.nombre_comun.lower())
        only_ascii = nfkd_form.encode('ASCII', 'ignore')
        only_ascii = only_ascii.decode("utf-8")
        return '{}{}'.format(only_ascii, extension)

    def upload(self, *args, **kwargs):
        self.archivo_pdf.name = self.get_name_file()
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        newName = self.get_name_file()
        if os.path.isfile('pdfs/{}'.format(newName)):
            os.remove('pdfs/{}'.format(newName))
        self.archivo_pdf.name = newName
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre_comun

    class Meta:
        verbose_name = 'Polen'
        verbose_name_plural = 'Polen'


class ReporteConcentracion(models.Model):
    fecha = models.DateTimeField(default=django.utils.timezone.now)
    tiempo_total = models.IntegerField(default=1440)
    tiempo_extra = models.IntegerField()
    porcentaje_muestreado = models.FloatField(default=0.1)
    niveles_polen = models.ManyToManyField(Polen, through='NivelesPolen', related_name='reportes')
    tiempo_real = models.FloatField()
    vol_polen = models.FloatField()
    vol_esporas_hongos = models.FloatField()

    def save(self, *args, **kwargs):
        self.tiempo_real = (self.tiempo_total + self.tiempo_extra) * self.porcentaje_muestreado
        self.vol_polen = (2.2*2400*self.tiempo_real*math.pi*8.21*0.159)/1000000
        self.vol_esporas_hongos = (2.2*2400*self.tiempo_real*math.pi*8.21*0.159)/6000000
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.fecha)

    class Meta:
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'


@receiver(post_save, sender=ReporteConcentracion)
def send_new_report_notification(sender, **kwargs):
    send_push_notification(
        User.objects.filter(notificaciones__in=[1]),
        critical_reports['title'],
        critical_reports['body'],
    )


class NivelesPolen(models.Model):
    reporte = models.ForeignKey(ReporteConcentracion, on_delete=models.CASCADE)
    polen = models.ForeignKey(Polen, on_delete=models.CASCADE)
    nivel = models.FloatField()
    nivel_calculado = models.FloatField()

    def save(self, *args, **kwargs):
        if self.polen.grupo_polinico.id == 'a' or self.polen.grupo_polinico.id == 'h':
            self.nivel_calculado = self.nivel / self.reporte.vol_polen
        else:
            self.nivel_calculado = self.nivel / self.reporte.vol_esporas_hongos
        super().save(*args, **kwargs)

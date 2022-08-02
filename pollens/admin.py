from django.contrib import admin
from .models import GrupoPolinico, Polen, ReporteConcentracion


class NivelesPolenInline(admin.TabularInline):
    model = ReporteConcentracion.niveles_polen.through
    fields = ['polen', 'nivel']


class ReporteAdmin(admin.ModelAdmin):
    inlines = [
        NivelesPolenInline,
    ]
    exclude = ('niveles_polen',)
    list_display = ['fecha', 'tiempo_real', 'vol_polen', 'vol_esporas_hongos']
    fieldsets = (
        (
            'tiempo_real',
            {
                'fields':
                (
                    'fecha',
                    'tiempo_total',
                    'tiempo_extra',
                    'porcentaje_muestreado',

                )
            }
        ),
    )


admin.site.register(ReporteConcentracion, ReporteAdmin)
admin.site.register(Polen)
admin.site.register(GrupoPolinico)

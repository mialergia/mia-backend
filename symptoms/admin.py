from django.contrib import admin

from .models import (
    ValorRespuesta,
)


class ValorRespuestaInline(admin.TabularInline):
    model = ValorRespuesta
    extra = 2


class EntradaDiarioAdmin(admin.ModelAdmin):
    inlines = (ValorRespuestaInline,)


# admin.site.register(TipoRespuesta)
# admin.site.register(Pregunta)
# admin.site.register(Historial)
# admin.site.register(EntradaDiario, EntradaDiarioAdmin)

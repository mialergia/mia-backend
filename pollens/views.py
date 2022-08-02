from rest_framework import viewsets

from .models import ReporteConcentracion, Polen
from .serializers import ReportSerializer, ReportDetailSerializer, TipoPolinicoSerializer


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = ReporteConcentracion.objects.all().order_by('-fecha')[:1]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"current_user": self.request.user})
        return context


class ReportDetailViewSet(viewsets.ModelViewSet):
    serializer_class = ReportDetailSerializer
    queryset = ReporteConcentracion.objects.all().order_by('-fecha')[:1]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "group_id": self.kwargs.get('group_id')
            }
        )
        return context


class PolenViewSet(viewsets.ModelViewSet):
    serializer_class = TipoPolinicoSerializer
    queryset = Polen.objects.all().filter(picks_presente=True)


class PolenPDFViewSet(viewsets.ModelViewSet):
    serializer_class = TipoPolinicoSerializer
    queryset = Polen.objects.all()

    def get_queryset(self):
        grupo_polinico = self.kwargs.get('group_id')
        events = Polen.objects.exclude(
                    archivo_pdf__isnull=True
                ).exclude(
                    archivo_pdf__exact=""
                ).filter(grupo_polinico=grupo_polinico)
        return events

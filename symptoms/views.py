from rest_framework import viewsets
from django.contrib.gis.geos import Point
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from datetime import timedelta, datetime

from .models import (
    Sintoma,
    Historial,
    EntradaDiario,
    CategoriaSintoma,
    Pregunta,
    ValorRespuesta
)
from .serializers import (
    HistorialSerializer,
    SintomaSerializer,
    EntradaDiarioSerializer,
    CategoriaSintomaSerializer,
    PreguntaSerializer
)
import alergias.strings as strings


class SintomaViewSet(viewsets.ModelViewSet):
    serializer_class = SintomaSerializer
    queryset = Sintoma.objects.all()


class HistorialViewSet(viewsets.ModelViewSet):
    serializer_class = HistorialSerializer
    queryset = Historial.objects.all()

    def perform_create(self, serializer):
        current_user = self.request.user
        current_user.necesita_onboarding = False
        current_user.save()
        serializer.save(usuario=current_user)

    def get_queryset(self):
        user = self.request.user
        events = Historial.objects.filter(usuario=user)
        return events


class CategoriaSintomaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSintomaSerializer
    queryset = CategoriaSintoma.objects.all().prefetch_related('sintoma_set')


class EntradaDiarioViewSet(viewsets.ModelViewSet):
    serializer_class = EntradaDiarioSerializer
    queryset = EntradaDiario.objects.all()

    def filter_queryset(self, queryset):
        queryset = super(EntradaDiarioViewSet, self).filter_queryset(queryset)
        return queryset.order_by('-fecha')

    def get_critical_answers_amount(self, entry):
        critical_answer_1 = Q(respuesta='si')
        critical_answer_2 = Q(respuesta='mucho')

        last_critical_answers_added = entry.valorrespuesta_set.filter(
            critical_answer_1 | critical_answer_2
        ).count()

        return last_critical_answers_added

    def get_alert(self):
        user_entries = self.get_queryset()
        last_critical_answers_added = self.get_critical_answers_amount(user_entries.last())

        one_week_ago = datetime.today() - timedelta(days=7)
        last_week_entries = user_entries.filter(fecha__gte=one_week_ago)

        last_week_critical_days = 0
        for entry in last_week_entries:
            enrty_critical_amount = self.get_critical_answers_amount(entry)

            if (enrty_critical_amount > 0):
                last_week_critical_days += 1

        alert = None
        if (last_week_critical_days > 4):
            alert = strings.high_critical_alert
        elif (last_critical_answers_added > 2):
            alert = strings.medium_critical_alert
        elif (last_critical_answers_added > 0):
            alert = strings.low_critical_alert

        return alert

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        alert = self.get_alert()
        serializer_with_alert = {'alerta': alert, 'entradas': serializer.data}

        return Response(serializer_with_alert, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        validated_data = serializer.validated_data

        if (validated_data.get('coordenadas')):
            coordenadas = validated_data['coordenadas']
            validated_data['coordenadas'] = Point(
                coordenadas['longitud'],
                coordenadas['latitud'],
            )

        serializer.save(usuario=self.request.user)

    def get_queryset(self):
        user = self.request.user
        events = EntradaDiario.objects.filter(usuario=user)
        return events

    def perform_destroy(self, instance):
        diary_entry_id = instance.id
        ValorRespuesta.objects.filter(entrada_diario=diary_entry_id).delete()
        instance.delete()


class PreguntaViewSet(viewsets.ModelViewSet):
    serializer_class = PreguntaSerializer
    queryset = Pregunta.objects.all().select_related('tipo_respuesta')

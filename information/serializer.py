from rest_framework import serializers

from .models import TerminosCondiciones, Notificacion


class TerminosCondicionesSerializer(serializers.ModelSerializer):

    class Meta:
        model = TerminosCondiciones
        fields = '__all__'


class NotificacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notificacion
        fields = '__all__'

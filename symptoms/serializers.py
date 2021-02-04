from rest_framework import serializers

from .models import (
    Historial,
    Sintoma,
    EntradaDiario,
    CategoriaSintoma,
    Pregunta,
    ValorRespuesta,
)


class SintomaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sintoma
        fields = (
            'id',
            'nombre',
            'descripcion',
            'categoria',
        )


class HistorialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Historial
        fields = (
            'id',
            'sintomas',
        )


class CategoriaSintomaSerializer(serializers.ModelSerializer):
    sintomas = SintomaSerializer(many=True, read_only=True, source='sintoma_set')

    class Meta:
        model = CategoriaSintoma
        fields = ('id', 'identificador', 'pregunta', 'sintomas')


class PreguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = (
            'id',
            'pregunta',
            'tipo_respuesta',
            'respuestas',
        )

    respuestas = serializers.SerializerMethodField('get_answer_options')

    def get_answer_options(self, obj):
        return obj.tipo_respuesta.opciones


class ValorRespuestaSerializer(serializers.ModelSerializer):
    valor_pregunta = serializers.SlugRelatedField(read_only=True, slug_field='pregunta', source='pregunta')

    class Meta:
        model = ValorRespuesta
        fields = (
            'id',
            'pregunta',
            'respuesta',
            'valor_pregunta',
        )


class EntradaDiarioSerializer(serializers.ModelSerializer):
    latitud = serializers.FloatField(write_only=True, required=False, allow_null=True)
    longitud = serializers.FloatField(write_only=True, required=False, allow_null=True)
    respuestas = ValorRespuestaSerializer(many=True, source='valorrespuesta_set')

    class Meta:
        model = EntradaDiario
        fields = (
            'id',
            'fecha',
            'coordenadas',
            'comentario',
            'latitud',
            'longitud',
            'respuestas',
        )

    def create(self, validated_data):
        respuestas = validated_data.pop('valorrespuesta_set')
        entrada_diario = EntradaDiario.objects.create(**validated_data)

        for respuesta in respuestas:
            ValorRespuesta.objects.create(entrada_diario=entrada_diario, **respuesta)

        return entrada_diario

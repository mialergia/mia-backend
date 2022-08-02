from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework.exceptions import ValidationError

from .models import User
import alergias.strings as strings


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    name = serializers.CharField(required=False)
    gender = serializers.ChoiceField(
        choices=User.OPCIONES_SEXO,
        required=False
    )
    date_of_birth = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    onesignal_player_id = serializers.CharField(required=False)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'email': self.validated_data.get('email', ''),
            'nombre': self.validated_data.get('nombre', ''),
            'sexo': self.validated_data.get('sexo', ''),
            'fecha_nacimiento': self.validated_data.get('fecha_nacimiento', ''),
            'departamento': self.validated_data.get('departamento', ''),
            'barrio': self.validated_data.get('barrio', ''),
            'password1': self.validated_data.get('password1', ''),
            'onesignal_player_id': self.validated_data.get('onesignal_player_id', ''),
        }


class UserDetailSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(required=True)
    departamento = serializers.CharField(required=True)
    fecha_nacimiento = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'nombre',
            'sexo',
            'fecha_nacimiento',
            'departamento',
            'barrio',
            'necesita_onboarding',
            'alergias',
            'onesignal_player_id',
            'notificaciones'
        )
        read_only_fields = ['email', 'necesita_onboarding']

    def update_many_to_many_relation(self, instance, saved_values, new_values, attribute_name):
        if (isinstance(new_values, list)):
            # remove old
            for saved_value in saved_values:
                getattr(instance, attribute_name).remove(saved_value)

            # add new
            for new_value in new_values:
                getattr(instance, attribute_name).add(new_value.id)

    def update(self, instance, validated_data):
        alergias = validated_data.get('alergias', instance.alergias)
        notificaciones = validated_data.get('notificaciones', instance.notificaciones)
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.sexo = validated_data.get('sexo', instance.sexo)
        instance.fecha_nacimiento = validated_data.get('fecha_nacimiento', instance.fecha_nacimiento)
        instance.onesignal_player_id = validated_data.get('onesignal_player_id', instance.onesignal_player_id)
        instance.departamento = validated_data.get('departamento', instance.departamento)
        instance.barrio = validated_data.get('barrio', instance.barrio)

        self.update_many_to_many_relation(instance, instance.alergias.all(), alergias, 'alergias')
        self.update_many_to_many_relation(instance, instance.notificaciones.all(), notificaciones, 'notificaciones')

        instance.save()
        return instance

    def validate_departamento(self, value):
        barrio = self.initial_data.get('barrio')

        if value.lower() == 'montevideo' and not barrio:
            raise ValidationError(strings.valid_neighboor)
        return value

from rest_framework import serializers
import os

from .models import ReporteConcentracion, GrupoPolinico, Polen


class PollenGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = GrupoPolinico
        fields = ('id', 'nombre')


class TipoPolinicoSerializer(serializers.ModelSerializer):
    grupo_polinico = PollenGroupSerializer(read_only=True)
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = Polen
        fields = (
            'id',
            'nombre_comun',
            'nombre_alergia',
            'grupo_polinico',
            'pdf_url'
        )

    def get_pdf_url(self, polen):
        request = self.context.get('request')
        pdf_url = polen.archivo_pdf_url
        if (pdf_url and os.path.isfile(pdf_url)):
            return request.build_absolute_uri('/{}'.format(pdf_url))
        return None


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteConcentracion
        fields = ('id', 'fecha')

    def get_polen_level(self, nivel_polen, affected_allergies, allergies_level,
                        total_polen, high_level_sum, medium_level_sum):
        current_user = self.context['current_user']
        grupo_polinico = nivel_polen.polen.grupo_polinico
        polen = nivel_polen.polen
        nivel_calculado = nivel_polen.nivel_calculado

        total_polen += nivel_calculado
        if (nivel_calculado > polen.nivel_alto) or (
            grupo_polinico.nivel_alto_sumatoria and
            total_polen > grupo_polinico.nivel_alto_sumatoria
        ):
            if nivel_calculado > polen.nivel_alto and polen in current_user.alergias.all():
                allergies_level = 'alto'
            high_level_sum += 1
        elif (nivel_calculado >= polen.nivel_medio or
                (grupo_polinico.nivel_medio_sumatoria and
                    total_polen > grupo_polinico.nivel_medio_sumatoria)):
            medium_level_sum += 1
            if (nivel_calculado >= polen.nivel_medio and nivel_calculado != 'alto'
                    and polen in current_user.alergias.all()):
                allergies_level = 'medio'
        if (nivel_calculado > polen.nivel_alto or nivel_calculado >= polen.nivel_medio):
            affected_allergies.append({
                "id": polen.id,
                "nombre_comun": polen.nombre_comun,
                "nombre_alergia": polen.nombre_alergia
            })
        if high_level_sum >= grupo_polinico.nivel_alto:
            return 'alto', affected_allergies, allergies_level, total_polen, high_level_sum, medium_level_sum
        elif medium_level_sum >= grupo_polinico.nivel_medio:
            return 'medio', affected_allergies, allergies_level, total_polen, high_level_sum, medium_level_sum
        else:
            return 'bajo', affected_allergies, allergies_level, total_polen, high_level_sum, medium_level_sum

    def to_representation(self, instance):
        # arboles
        high_level_sum_a = 0
        medium_level_sum_a = 0
        total_polen_a = 0
        trees_level = 'bajo'

        # hierbas
        high_level_sum_h = 0
        medium_level_sum_h = 0
        total_polen_h = 0
        grass_level = 'bajo'

        # hongos
        high_level_sum_g = 0
        medium_level_sum_g = 0
        total_polen_g = 0
        mushrooms_level = 'bajo'

        affected_allergies = []
        allergies_level = 'bajo'

        for nivel_polen in instance.nivelespolen_set.all():
            grupo_polinico = nivel_polen.polen.grupo_polinico

            # arboles
            if grupo_polinico.id == 'a':
                (trees_level, affected_allergies, allergies_level, total_polen_a, high_level_sum_a,
                    medium_level_sum_a) = self.get_polen_level(
                    nivel_polen, affected_allergies, allergies_level,
                    total_polen_a, high_level_sum_a, medium_level_sum_a)

            # hierbas
            elif grupo_polinico.id == 'h':
                (grass_level, affected_allergies, allergies_level, total_polen_h, high_level_sum_h,
                    medium_level_sum_h) = self.get_polen_level(
                    nivel_polen, affected_allergies, allergies_level,
                    total_polen_h, high_level_sum_h, medium_level_sum_h)

            # hongos
            elif grupo_polinico.id == 'g':
                (mushrooms_level, affected_allergies, allergies_level, total_polen_g, high_level_sum_g,
                    medium_level_sum_g) = self.get_polen_level(
                    nivel_polen, affected_allergies, allergies_level,
                    total_polen_g, high_level_sum_g, medium_level_sum_g)

        ret = super(ReportSerializer, self).to_representation(instance)
        extra_ret = {
            "niveles": [
                {"id": "a", "name": "arboles", "nivel": trees_level},
                {"id": "h", "name": "hierbas", "nivel": grass_level},
                {"id": "g", "name": "hongos", "nivel": mushrooms_level}
            ],
            "alerta": {
                "alergias": affected_allergies,
                "nivel": allergies_level
            }
        }
        ret.update(extra_ret)
        return ret


class ReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteConcentracion
        fields = ('id', 'fecha')

    def get_pdf_url(self, polen):
        request = self.context.get('request')
        pdf_url = polen.archivo_pdf_url
        if (pdf_url and os.path.isfile(pdf_url)):
            return request.build_absolute_uri('/{}'.format(pdf_url))
        return None

    def createPolenJson(self, polen, nivel):
        return {
            "id": polen.id,
            "nombre_comun": polen.nombre_comun,
            "nombre_alergia": polen.nombre_alergia,
            "pdf_url": self.get_pdf_url(polen),
            "nivel": nivel
        }

    def to_representation(self, instance):
        group_id = self.context['group_id']

        high_level = []
        medium_level = []
        low_level = []

        for nivel_polen in instance.nivelespolen_set.all():
            grupo_polinico = nivel_polen.polen.grupo_polinico
            polen = nivel_polen.polen
            nivel_calculado = nivel_polen.nivel_calculado

            if grupo_polinico.id == group_id:
                if nivel_calculado > polen.nivel_alto:
                    high_level.append(self.createPolenJson(polen, 'alto'))
                elif nivel_calculado >= polen.nivel_medio:
                    medium_level.append(self.createPolenJson(polen, 'medio'))
                else:
                    low_level.append(self.createPolenJson(polen, 'bajo'))

        niveles = high_level + medium_level + low_level
        ret = super(ReportDetailSerializer, self).to_representation(instance)
        extra_ret = {"niveles": niveles}
        ret.update(extra_ret)
        return ret

from django.test import TestCase
from rest_framework import status
from faker import Faker
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import ModelAdmin

from pollens.tests.factories import GrupoPolinicoFactory
from users.tests.factories import UserFactory
from pollens.models import GrupoPolinico
from alergias.utils import get_random_choices
from pollens.serializers import PollenGroupSerializer


class MockRequest:
    pass

fake = Faker()
request = MockRequest()


class TestPollenGroup(TestCase):

    @classmethod
    def setUp(self):
        # self.pollen_group_url = reverse('grupopolinico-list')
        self.client_test = APIClient()
        self.user = UserFactory()
        self.client_test.force_authenticate(self.user)
        self.site = AdminSite()
        self.model_admin = ModelAdmin(GrupoPolinico, self.site)
        # symptoms_id = [symptom.id for symptom in Sintoma.objects.all()]
        # self.symptoms_selected = get_random_choices(symptoms_id, 5)

    def test_pollen_group_model(self):
        self.assertEqual(str(self.model_admin), 'pollens.ModelAdmin')
    
    # def test_default_fields(self):
    #     self.assertEqual(
    #         list(self.model_admin.get_fields(request).base_fields),
    #         [
    #             'id',
    #             'nombre', 
    #             'unidad_medida',
    #             'nivel_alto',
    #             'nivel_medio',
    #             'nivel_alto_sumatoria',
    #             'nivel_medio_sumatoria',
    #         ]
    #     )
        # import pdb; pdb.set_trace()

    def test_create_pollen_group(self):
        id = 'gp_id'
        name = fake.word()
        metric_unit = fake.text(max_nb_chars=12)
        high_level = fake.random_int()
        medium_level = fake.random_int()
        sum_medium_level = fake.random_int()
        sum_high_level = fake.random_int()

        response = self.client_test.post(
            reverse('admin:pollens_grupopolinico_add'),
            {
                'id': id,
                'nombre': name, 
                'unidad_medida': metric_unit,
                'nivel_alto': high_level,
                'nivel_medio': medium_level,
                'nivel_medio_sumatoria': sum_medium_level,
                'nivel_alto_sumatoria': sum_high_level,
            },
            format='json',
            follow=True,
        )
        print(response)

        import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # #     db_history = HistorialSerializer(Historial.objects.first()).data
    # #     response_history = response.data

    # #     self.assertEqual(response_history, db_history)

    # # def test_create_history_with_empty_symptoms(self):
    # #     response = self.client_test.post(
    # #         self.history_url
    # #     )

    # #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # #     db_history = HistorialSerializer(Historial.objects.first()).data
    # #     response_history = response.data

    # #     self.assertEqual(response_history, db_history)

    # # def test_get_history(self):
    # #     HistoryFactory.create_batch(10, symptoms=self.symptoms_selected, usuario=self.user)
    # #     response = self.client_test.get(self.history_url)
    # #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # #     db_history = HistorialSerializer(Historial.objects.all(), many=True).data
    # #     response_history = response.data

    # #     self.assertEqual(response_history, db_history)

    # # def test_delete_symptom(self):
    # #     HistoryFactory(symptoms=self.symptoms_selected, usuario=self.user)
    # #     history_id = Historial.objects.first().id

    # #     response = self.client_test.delete(f'{self.history_url}{history_id}/')
    # #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    # #     self.assertIsNone(Historial.objects.first())

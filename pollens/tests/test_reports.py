from django.test import TestCase
from rest_framework import status
from faker import Faker
from rest_framework.test import APIClient
from django.urls import reverse

from users.tests.factories import UserFactory
from pollens.tests.factories import ConcentrationReportWithPollenLevelFactory
from pollens.models import GrupoPolinico, ReporteConcentracion
from pollens.serializers import ReportSerializer, ReportDetailSerializer
from alergias.utils.tests import get_random_choices

fake = Faker()


class TestSymptoms(TestCase):
    fixtures = [
        'pollens/fixtures/grupos_polinicos.json',
        'pollens/fixtures/polens.json',
    ]

    @classmethod
    def setUp(self):
        self.report_url = reverse('reporteconcentracion-list')
        self.client_test = APIClient()
        self.user = UserFactory()
        self.client_test.force_authenticate(self.user)

    def test_get_report(self):
        ConcentrationReportWithPollenLevelFactory()
        response = self.client_test.get(self.report_url)

        db_report = ReportSerializer(
            ReporteConcentracion.objects.all(),
            many=True,
            context={"current_user": self.user}
        ).data
        response_report = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response_report)
        self.assertEqual(response_report, db_report)

    def test_get_report_detail(self):
        ConcentrationReportWithPollenLevelFactory()
        pollen_group_id = get_random_choices(GrupoPolinico.objects.all(), 1)[0].id
        response = self.client_test.get(f'{self.report_url}detail/{pollen_group_id}/')

        db_report_detail = ReportDetailSerializer(
            ReporteConcentracion.objects.all(),
            many=True,
            context={"group_id": pollen_group_id}
        ).data
        response_report_detail = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response_report_detail)
        self.assertEqual(response_report_detail, db_report_detail)

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.views.generic.base import TemplateView
import environ

from .models import TerminosCondiciones, Notificacion
from .serializer import TerminosCondicionesSerializer, NotificacionSerializer


class TerminosCondicionesViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = TerminosCondicionesSerializer
    queryset = TerminosCondiciones.objects.all()


class OnesignalView(TemplateView):
    template_name = 'onesignal/base_registered.html'

    def get_context_data(self, **kwargs):
        env = environ.Env(ONESIGNAL_APP_ID=str)
        environ.Env.read_env()

        context = super().get_context_data(**kwargs)
        context['onesignal_app_id'] = env('ONESIGNAL_APP_ID')

        return context


class NotificacionView(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    queryset = Notificacion.objects.all()

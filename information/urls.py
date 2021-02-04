from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from django.urls import include, path

from .views import TerminosCondicionesViewSet, OnesignalView, NotificacionView

router = DefaultRouter()
router.register(r'terms_conditions', TerminosCondicionesViewSet)
router.register(r'notifications', NotificacionView)

urlpatterns = [
    path('', include(router.urls)),
    path('manifest.json', TemplateView.as_view(
        template_name='onesignal/manifest.json',
        content_type='application/json')
    ),
    path('OneSignalSDKWorker.js', TemplateView.as_view(
        template_name='onesignal/OneSignalSDKWorker.js',
        content_type='application/x-javascript')
    ),
    path('OneSignalSDKWorker.js', TemplateView.as_view(
        template_name='onesignal/OneSignalSDKWorker.js',
        content_type='application/x-javascript')
    ),
    path('onesignal_web', OnesignalView.as_view()),
]

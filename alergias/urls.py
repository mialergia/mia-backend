from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from files.views import send_file

from alergias.cron import cron_send_drips

cron_send_drips()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('terminos_condiciones/', TemplateView.as_view(template_name='terminos_condiciones.html')),
    path('pdfs/<str:filename>', send_file),
]

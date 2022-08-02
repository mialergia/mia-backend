from rest_framework.routers import DefaultRouter

from symptoms.views import (
    SintomaViewSet,
    HistorialViewSet,
    EntradaDiarioViewSet,
    CategoriaSintomaViewSet,
    PreguntaViewSet,
)

router = DefaultRouter()
router.register(r'category_symptoms', CategoriaSintomaViewSet)
router.register(r'simptoms', SintomaViewSet)
router.register(r'historial', HistorialViewSet)
router.register(r'diary', EntradaDiarioViewSet)
router.register(r'questions', PreguntaViewSet)

urlpatterns = router.urls

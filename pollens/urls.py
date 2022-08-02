from rest_framework.routers import DefaultRouter

from pollens.views import ReportViewSet, ReportDetailViewSet, PolenViewSet, PolenPDFViewSet

router = DefaultRouter()
router.register(r'report', ReportViewSet)
router.register(r'report/detail/(?P<group_id>\D+)', ReportDetailViewSet)
router.register(r'allergies', PolenViewSet)
router.register(r'pdfs/(?P<group_id>\D+)', PolenPDFViewSet)

urlpatterns = router.urls

from rest_framework import routers
from django.urls import include, re_path, path
from .views import BoardViewSet, RegionViewSet, ConditionViewSet, DivisionViewSet, UserViewSets, VerificationAPIView

router = routers.SimpleRouter()
router.register('board', BoardViewSet)
router.register('region', RegionViewSet)
router.register('division', DivisionViewSet)
router.register('condition', ConditionViewSet)
router.register('user', UserViewSets)

urlpatterns = [
    path('user/verification/email/', VerificationAPIView.as_view()),
    re_path(r'^auth/', include('djoser.urls.authtoken'))
              ] + router.urls


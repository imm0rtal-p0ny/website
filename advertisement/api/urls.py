from rest_framework import routers
from .views import BoardViewSet, RegionViewSet, ConditionViewSet, DivisionViewSet

router = routers.SimpleRouter()
router.register('board', BoardViewSet)
router.register('region', RegionViewSet)
router.register('division', DivisionViewSet)
router.register('condition', ConditionViewSet)

urlpatterns = [] + router.urls


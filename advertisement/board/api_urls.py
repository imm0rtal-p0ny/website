from rest_framework import routers
from .api import BoardViewSet, RegionViewSet, StatusViewSet, DivisionViewSet, ConditionViewSet

router = routers.DefaultRouter()
router.register('boards', BoardViewSet)
router.register('boards', BoardViewSet)
router.register('statuses', StatusViewSet)
router.register('regions', RegionViewSet)
router.register('divisions', DivisionViewSet)
router.register('conditions', ConditionViewSet)

urlpatterns = router.urls

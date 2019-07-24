from django.conf.urls import url, include
from rest_framework import routers
from .views import StationViewSet,StationRealtimeListView,BigmeterViewSet,OrganizationsViewSet


router = routers.DefaultRouter()
router.register(r'stations', StationViewSet)
router.register(r'bigmeter', BigmeterViewSet)

# urlpatterns = router.urls

app_name='api-dmam'

urlpatterns = [
    url('', include(router.urls)),
    url('realtimedata/', StationRealtimeListView.as_view(), name='realtime'),
    url('bigmeter/', BigmeterViewSet.as_view({'get': 'list'}), name='bigmeter'),
    url('organizations/', OrganizationsViewSet.as_view({'get': 'list'}), name='organizations'),
]
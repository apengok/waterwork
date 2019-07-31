# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from .views import FenceDistrictViewSet,FenceShapeViewSet,FenceShapeCollectionViewSet


router = routers.DefaultRouter()
router.register(r'district', FenceDistrictViewSet)
router.register(r'fences', FenceShapeViewSet)
router.register(r'collections', FenceShapeCollectionViewSet)

# urlpatterns = router.urls

app_name='api-ggis'

urlpatterns = [
    url('', include(router.urls)),
    # url('realtimedata/', StationRealtimeListView.as_view(), name='realtime'),
    # url('bigmeter/', BigmeterViewSet.as_view({'get': 'list'}), name='bigmeter'),
    # url('organizations/', OrganizationsViewSet.as_view({'get': 'list'}), name='organizations'),
]
from django.conf.urls import url, include
from rest_framework import routers
from .views import AlarmViewSet


router = routers.DefaultRouter()
router.register(r'alarms', AlarmViewSet)

urlpatterns = router.urls

app_name='api-legacy'
from django.conf.urls import url


from .views import UserViewSet

app_name = 'api-account'
urlpatterns = [
    url(r'^user/$', UserViewSet.as_view({'get':'list'}), name='user-listcreate'),
    # url(r'^(?P<pk>\d+)/$', BlogPostRudView.as_view(), name='post-rud')
]   
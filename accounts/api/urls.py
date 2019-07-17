from django.conf.urls import url


from .views import (
    UserViewSet,
    UserListView,
    UserDetailView,
    UserAllOpView,
    UserCreateView,
    UserUpdateView
)

app_name = 'api-account'
urlpatterns = [
    url(r'^user/$', UserViewSet.as_view({'get':'list'}), name='user-listcreate'),
    url(r'^user/list/$', UserListView.as_view(), name='user-list'),
    url(r'^user/(?P<pk>\d+)/$', UserDetailView.as_view(), name='user-detail'),
    url(r'^user/(?P<pk>\d+)/op/$', UserAllOpView.as_view(), name='user-allop'),
    url(r'^user/(?P<pk>\d+)/update/$', UserUpdateView.as_view(), name='user-update'),
    url(r'^user/create/$', UserCreateView.as_view(), name='user-create'),

    # url(r'^(?P<pk>\d+)/$', BlogPostRudView.as_view(), name='post-rud')
]   
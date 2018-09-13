from django.urls import path
from django.conf.urls import url
from home import views

urlpatterns = [
    url(r'^list', views.list, name='list'),
    url(r'^create', views.create, name='create'),
    url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit'),
]
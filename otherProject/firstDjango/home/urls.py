from django.urls import path
from django.conf.urls import url
from home import views

urlpatterns = [
    #path('', views.index, name='index') #localhost/home 까지만 치면 나오는 화면.
    url(r'^contact', views.contact),
    url(r'^about', views.about)
]

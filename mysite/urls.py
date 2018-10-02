"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth import views

#프로젝트의 종합 기본 경로 지정.
#큰 분류/대분류를 지정하는 곳.
urlpatterns = [
    re_path(r'^admin/', admin.site.urls),

    # 만약 r'' 를 r'^blog/' 로 지정했다면, URL이 http://~~/blog/ 까지는 여기서 지정한 것까지 붙고,
    # 이다음 blog/~의  ~이하 경로는 blog.urls 파일에서 지정한 경로들이 자동으로 붙는다.
    re_path(r'^blog/', include('blog.urls')), # 해당 경로 아래 blog.urls에 지정된 경로가 붙는다.

    #re_path(r'^accounts/', include('django.contrib.auth.urls')), # 장고의 가장 기본적인 로그인/아웃등의 인증 처리 url 설정.
    # re_path(r'^accounts/login/$', views.login, name='login'),
    # #kwargs의 next_page 값 : 로그아웃 후, 이동할 url
    # re_path(r'^accounts/logout/$', views.auth_logout(), name='logout', kwargs={'next_page': '/'}),
]

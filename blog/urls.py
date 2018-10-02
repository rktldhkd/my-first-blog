# -*- coding: utf-8 -*-

from django.urls import path, re_path, include
from . import views

#아래 2개 : 업로드파일, 이미지첨부기능위함.
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    re_path(r'^$', views.post_list, name='post_list'),
    # ^은 "시작"을 뜻합니다.
    # post/란 URL이 post 문자를 포함해야 한다는 것을 말합니다. 아직 할 만하죠?
    # (?P<pk>\d+)는 조금 까다롭습니다. 이 정규표현식은 장고가 pk변수에 모든 값을 넣어 뷰로 전송하겠다는 뜻입니다.
    # \d은 문자를 제외한 숫자 0부터 9 중, 한 가지 숫자만 올 수 있다는 것을 말합니다.
    # +는 하나 또는 그 이상의 숫자가 올 수 있습니다.. 따라서 http://127.0.0.1:8000/post/라고 하면
    # post/ 다음에 숫자가 없으므로 해당 사항이 아니지만, http://127.0.0.1:8000/post/1234567890/는 완벽하게 매칭됩니다.
    # /은 다음에 / 가 한 번 더 와야 한다는 의미입니다.
    # $는 "마지막"을 말합니다. 그 뒤로 더는 문자가 오면 안 됩니다.
    re_path(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    re_path(r'^post/new/$', views.post_new, name='post_new'),
    re_path(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    re_path(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    re_path(r'^post/(?P<pk>\d+)/comment/add/$', views.add_comment_to_post, name="add_comment_to_post"),
    re_path(r'^login/$', views.login, name='login'), # 로그인 url
    re_path(r'^logout/$', views.logout, name='logout'), # 로그아웃 url
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^download_file/(?P<file_name>.*)/$', views.download_file, name='download_file'),
    #?P<file_name>\w{0,50}) : 문자만 받는다., .* : 전부 다 받는다.
]

#static 파일과는 다르게 개발서버에서 기본 서빙 미지원
#개발 편의성 목적으로 서빙 rule 추가 가능
#settings.DEBUG = False 일때는 static 함수에서 빈 리스트 리턴
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #업로드파일, 이미지첨부기능위함.
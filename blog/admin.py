# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Post, Comment, Profile

# Register your models here.
# 만든 모델을 관리자 페이지에서 보려면 admin.site.register(Post)로 모델을 등록해야 해요.
# 모델을 적절하게 등록해주지 않으면 관리자 화면에서 로그인할 때 에러 발생한다.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)
# -*- coding: utf-8 -*-

import os
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
        login as django_login,
        logout as djangp_logout,
        authenticate
    )

from .models import Post, Profile
from .forms import PostForm, LoginForm, CommentForm, SignUpForm


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # render() : 이 함수는 호출하여 받은(return) blog/post_list.html템플릿을 보여줍니다.
    return render(request, 'blog/post_list.html', {'posts' : posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk) #pk에 해당하는 Post가 없을 경우, 멋진 페이지(페이지 찾을 수 없음 404 : Page Not Found 404)를 보여줄 거에요.
    return render(request, 'blog/post_detail.html', {'post' : post})


    # post = get_object_or_404(Post, pk=pk) #pk에 해당하는 Post가 없을 경우, 멋진 페이지(페이지 찾을 수 없음 404 : Page Not Found 404)를 보여줄 거에요.
    #
    # if post.file:
    #     fileName = post.file.name
    #     start     = fileName.rfind('/') + 1  # 역방향 검색, 파일명만...
    #     fileName  = fileName[start:]
    #
    # elif post.photo:
    #     photoName = post.photo.name
    #     start = photoName.rfind('/') + 1
    #     photoName = photoName[start:]
    #     return render(request, 'blog/post_detail.html', {'post' : post, 'fileName':fileName, 'photoName':photoName})
    # else:
    #     return render(request, 'blog/post_detail.html', {'post' : post, 'fileName':fileName, 'photoName':photoName})

@login_required#(login_url='/accounts/login/')
def post_new(request):
    # 폼을 제출할때, request에는 우리가 입력했던 데이터들을 가지고 있는데, request.POST가 이 데이터를가지고있습니다 -->
    # 이제 view 에서 두 상황으로 나누어 처리해볼게요.
    # 첫 번째: 처음 페이지에 접속했을 때입니다. 당연히 우리가 새 글을 쓸 수 있게 폼이 비어있어야겠죠.
    # 두 번째: 폼에 입력된 데이터를 view 페이지로 가지고 올 때입니다. 여기서 조건문을 추가시켜야 해요. (if를 사용하세요)
    if request.method == "POST":
        #파일 정보는 request.FILES 를 통해 전달된다.
        form = PostForm(request.POST, request.FILES)
        #폼에 들어있는 값들이 올바른지를 확인해야합니다.(모든 필드에는 값이 있어야하고 잘못된 값이 있다면 저장하면 되지
        # 않아야해요) 이를 위해 form.is_valid()을 사용할거에요.
        #폼에 입력된 값이 올바른지 확인한 다음, 저장되는거죠!
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form':form})

@login_required
def post_edit(request, pk):
    # 첫 번째: url로부터 추가로 pk 매개변수를 받아서 처리합니다.
    # 두 번째: get_object_or_404(Post, pk=pk)를 호출하여 수정하고자 하는 글의 Post 모델 인스턴스(instance)로
    # 가져옵니다. (pk로 원하는 글을 찾습니다) 이렇게 가져온 데이터를 폼을 만들 때와(글을 수정할 때 폼에 이전에
    # 입력했던 데이터가 있어야 하겠죠?) 폼을 저장할 때 사용하게 됩니다.
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST": # 2번째 이후부터 페이지에서 데이터를 넘겼을 때,
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else: #처음 페이지 접속 시,
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form' : form})

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.photo.delete()
    post.file.delete()
    post.delete()
    return redirect('post_list')

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid(): #form 데이터 유무 확인
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        # 현재 유저명 가져오기. 'author'는 forms.py에서 지정한 form 안의 fields속성의 값.
        # 여기 코드에서 건드릴 부분은 'author'와 user_id변수명 밖에 없고 나머지는 규격이다.
        # 여러 개를 보낼 땐, {}안의 값에 ,를 구분자로 여러 개 넣으면 될 듯하다.
        user_id = {'author' : request.user.username}
        # form에 데이터를 보내기 위해 파라미터를 지정했다.
        # initial 속성값을 지정해서 forms.py에 필요한 데이터를 보낸다.
        form = CommentForm(initial=user_id)
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


def login(request):
    if request.method == 'POST':
        # Data bounded form인스턴스 생성
        login_form = LoginForm(request.POST)
        # 유효성 검증에 성공할 경우
        if login_form.is_valid():
            # form으로부터 username, password값을 가져옴
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            # 가져온 username과 password에 해당하는 User가 있는지 판단한다
            # 존재할경우 user변수에는 User인스턴스가 할당되며,
            # 존재하지 않으면 None이 할당된다
            user = authenticate(
                username=username,
                password=password
            )
            # 인증에 성공했을 경우
            if user:
                # Django의 auth앱에서 제공하는 login함수를 실행해 앞으로의 요청/응답에 세션을 유지한다
                django_login(request, user)
                # Post목록 화면으로 이동
                return redirect('post_list')
            # 인증에 실패하면 login_form에 non_field_error를 추가한다
            login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
    else:
        login_form = LoginForm()
    context = {
        'login_form': login_form,
    }
    return render(request, 'registration/login.html', context)

@login_required
def logout(request):
    djangp_logout(request)
    return redirect('post_list')


# 회원가입 view
# Because of the Signal handling the Profile creation, we have a synchronism issue here.
# It is easily solved by calling the user.refresh_from_db() method. This will cause a hard refresh
# from the database, which will retrieve the profile instance.
# If you don’t call user.refresh_from_db(), when you try to access the user.profile, it will return None.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            # django.contrib.auth 모듈의 login 함수를 가져와야하는데
            # views.py에 login 함수가 정의되어있어서 views.py의 login함수가 호출되어진다.
            # 따라서 함수를 import할때 앨리어스명(auth_login)을 주어서 적절한 함수를 호출하게 했다.
            # login(request, user)
            django_login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def download_file(request, file_name):
    request.encoding = 'utf-8'
    start = file_name.rfind('/') + 1  # 역방향 검색, 파일명만...
    fileName = file_name[start:]
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    if os.path.exists(file_path):

        print("===========START DEBUG============")
        print("file_name : " + file_name)
        print("filename : " + fileName)
        print("file_path : " + file_path)
        print("file len : %d" % os.stat(file_path).st_size)
        print("x-sendfile : " + smart_str(file_path))
        print("===========END DEBUG==============")
        
        # 영문이름의 파일은 잘 다운되지만
        # 한글이 들어간 url경로가 깨지면서 이름에 한글이 들어간 파일은 다운로드가 되지 않는다.
        # x-sendfile 과 더불어 view에서 집어넣는 이름값들은 다 콘솔에서 한글 정상출력된다.
        # 하지만 url을 타서 화면을 보여줄 때, url에서 한글이 깨진다. 서버로 전송되면서 한글이 깨지는 현상인듯하다.
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            #response['X-Sendfile'] = file_path -원본
            response['content_type'] = 'charset=utf-8'
            response['X-Sendfile'] = smart_str(file_path)
            response['Content-Length'] = os.stat(file_path).st_size
            #response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path) -원본
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(fileName)
            return response


    #아래는 그냥 참고용. 아래꺼랑 위에꺼원본이랑 짜집기해서 파일다운로드기능 완성
    # file_path = os.path.join(settings.MEDIA_ROOT, fileName)
    # response = HttpResponse(open(file_path, 'rb').read())
    # response['Content-Type'] = 'text/plain'
    # response['Content-Disposition'] = 'attachment; filename=DownloadedText.txt'
    # return response

    # file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    # response = HttpResponse(content_type='application/force-download')
    # response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(fileName)
    # response['X-Sendfile'] = smart_str(file_path)
    # # It's usually a good idea to set the 'Content-Length' header too.
    # # You can also set any other required headers: Cache-Control, etc.
    # return response
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # render() : 이 함수는 호출하여 받은(return) blog/post_list.html템플릿을 보여줍니다.
    return render(request, 'blog/post_list.html', {'posts' : posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk) #pk에 해당하는 Post가 없을 경우, 멋진 페이지(페이지 찾을 수 없음 404 : Page Not Found 404)를 보여줄 거에요.
    return render(request, 'blog/post_detail.html', {'post' : post})

def post_new(request):
    # 폼을 제출할때, request에는 우리가 입력했던 데이터들을 가지고 있는데, request.POST가 이 데이터를가지고있습니다 -->
    # 이제 view 에서 두 상황으로 나누어 처리해볼게요.
    # 첫 번째: 처음 페이지에 접속했을 때입니다. 당연히 우리가 새 글을 쓸 수 있게 폼이 비어있어야겠죠.
    # 두 번째: 폼에 입력된 데이터를 view 페이지로 가지고 올 때입니다. 여기서 조건문을 추가시켜야 해요. (if를 사용하세요)
    if request.method == "POST":
        form = PostForm(request.POST)
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

def post_edit(request, pk):
    # 첫 번째: url로부터 추가로 pk 매개변수를 받아서 처리합니다.
    # 두 번째: get_object_or_404(Post, pk=pk)를 호출하여 수정하고자 하는 글의 Post 모델 인스턴스(instance)로
    # 가져옵니다. (pk로 원하는 글을 찾습니다) 이렇게 가져온 데이터를 폼을 만들 때와(글을 수정할 때 폼에 이전에
    # 입력했던 데이터가 있어야 하겠죠?) 폼을 저장할 때 사용하게 됩니다.
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form' : form})
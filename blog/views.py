from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # render() : 이 함수는 호출하여 받은(return) blog/post_list.html템플릿을 보여줍니다.
    return render(request, 'blog/post_list.html', {'posts' : posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk) #pk에 해당하는 Post가 없을 경우, 멋진 페이지(페이지 찾을 수 없음 404 : Page Not Found 404)를 보여줄 거에요.
    return render(request, 'blog/post_detail.html', {'post' : post})
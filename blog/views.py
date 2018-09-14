from django.shortcuts import render

# Create your views here.
def post_list(request):
    # render() : 이 함수는 호출하여 받은(return) blog/post_list.html템플릿을 보여줍니다.
    return render(request, 'blog/post_list.html', {})
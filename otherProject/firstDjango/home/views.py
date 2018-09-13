from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    '''

    첫번째 파라미터로 request를, 그리고 두번째 파라미터로 템플릿을 받아들인다. 여기서 템플릿은 index.html으로 지정되어 있는데,
    이는 home/templates/index.html을 가리키게 된다. 세번째 파라미터는 Optional 인데, View에서 템플릿에 전달한 데이타를
    Dictionary로 전달한다. Dictionary의 Key는 템플릿에서 사용할 키(or 변수명)이고,
    Value는 전달하는 데이타의 내용을 담는다. 여기서는 message 라는 키로 "My Message"라는 문자열을 전달하고 있다.
    :param request:
    :return:
    '''
    msg = 'My Message!'
    #django에서 templates 까지의 경로를 자동탐색한다. 따라서 templates 다음의 경로만 입력하여
    #템플릿을 탐색한다.
    return render(request, 'home/index.html', {'message' : msg})
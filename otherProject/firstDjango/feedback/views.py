from django.shortcuts import render, redirect
from .models import *
from .forms import FeedbackForm

# Create your views here.
# list와 edit을 간단히 설명하면, list 는 모든 Feedback 데이타를 가져와 feedbacklist.html
# 템플릿에 전달하여 전체 피드백 리스트를 작성한다. edit 는 id 를 URL에서 전달받아 (/feedback/edit/2 와 같이)
# 해당 id를 갖는 Feedback 데이타 하나를 feedback.html 템플릿에서 수정하게 한다.
#특히 edit() 함수에서 하나의 Feedback 객체를 Feedback.objects.get() 을 통해 가져온 후,
# 이를 FeedbackForm(instance=fb) 폼 생성자에 "instance=" 을 써서 전달하고 있음에 유의하자 (주: edit() 함수의 else 부분).
# 이렇게 하면 해당 Feedback 객체의 필드값들이 채워진 FeedbackForm 객체가 생성된다.
#또한, 편집 내용이 저장되어 POST로 전달될 때, FeedbackForm(request.POST, instance=fb) 와 같이 표현되고 있는데,
# 이는 save()시 해당 Feedback객체(fb)가 request.POST 데이타로 갱신되게 한다 (주: edit() 함수의 if 블럭).

def list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedbacklist.html', {'feedbacks' : feedbacks})


def create(request):
    if request.methos=='POST':
        form = FeedbackForm(request.POST)
        if form.is_valid(): # POST 데이타에 잘못된 데이타가 전달되었는지를 체크
            form.save()
        return redirect('/feedback/list')
    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {'form' : form})

def edit(request, id):
    fb = Feedback.objects.get(pk=id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=fb)
        if form.is_valid():
            form.save()
        return redirect('/feedback/list')
    else:
        form = FeedbackForm(instance=fb)
    return render(request, 'feedback.html', {'form' : form})
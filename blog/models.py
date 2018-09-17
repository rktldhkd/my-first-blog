from django.db import models
from django.utils import timezone

# Create your models here.

#class Post(models.Model):는 모델을 정의하는 코드입니다. (모델은 객체(object)라고 했죠?)

#class는 특별한 키워드로, 객체를 정의한다는 것을 알려줍니다.
#Post는 모델의 이름입니다. (특수문자와 공백 제외한다면) 다른 이름을 붙일 수도 있습니다.
#항상 클래스 이름의 첫 글자는 대문자로 써야 합니다.
#models은 Post가 장고 모델임을 의미합니다. 이 코드 때문에 장고는 Post가 데이터베이스에 저장되어야 한다고 알게 됩니다.
#이제 속성을 정의하는 것에 대해서 이야기해 볼게요. title, text, created_date, published_date, author에
# 대해서 말할 거에요. 속성을 정의하기 위해, 필드마다 어떤 종류의 데이터 타입을 가지는지를 정해야 해요.
# 여기서 데이터 타입에는 텍스트, 숫자, 날짜, 사용자 같은 다른 객체 참조 등이 있습니다.
# 하나의 클래스는 DB의 하나의 테이블과 같습니다.

#models.CharField - 글자 수가 제한된 텍스트를 정의할 때 사용합니다. 글 제목같이 짧은 문자열 정보를 저장할 때 사용합니다.
#models.TextField - 글자 수에 제한이 없는 긴 텍스트를 위한 속성입니다. 블로그 콘텐츠를 담기 좋겠죠?
#models.DateTimeField - 날짜와 시간을 의미합니다.
#models.ForeignKey - 다른 모델에 대한 링크를 의미합니다.


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()

    def __str__(self):
        return self.title
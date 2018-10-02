# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

# 게시글 테이블
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()

    file = models.FileField(blank=True, upload_to="blog/files/%Y/%m/%d")

    photo = models.ImageField(blank=True, null=True, upload_to="blog/images/%Y/%m/%d") #이미지 첨부기능
    # 저장경로 : MEDIA_ROOT/blog/2017/05/10/xxxx.jpg 경로에 저장
    # DB필드 : 'MEDIA_URL/blog/2017/05/10/xxxx.jpg' 문자열 저장

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()

    def __str__(self):
        return self.title


# 댓글 테이블
class Comment(models.Model):
    # models.ForeignKey의 related_name 옵션은 Post 모델에서 댓글에 액서스할 수 있게 합니다.
    # on_delete 설정 안해주면 해주라고 error 발생한다.
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

#회원가입 테이블
# One-To-One 관계는 이미 존재하는 어떤 Model에 대해 추가적인 정보를 저장할 필요가 있지만 그 Model의 핵심 역할과 크게
# 관련이 없는 경우 새로운 모델을 추가하고 One-To-One 관계로 연결하여 사용합니다.
# Django의 User Model의 경우, 인증 절차(the authentication process)와 관련이 없는 생일, 자기소개, 주소 등의
# Profile 정보를 추가할 때 주로 사용됩니다.
# One-To-One 관계로 연결된 모델은 User Model 과는 별개로 자체 데이터베이스 테이블을 가지게 됩니다.
class Profile(models.Model):
    # STUDENT = 1
    # TEACHER = 2
    # SUPERVISOR = 3
    # ROLE_CHOICES = (
    #     (STUDENT, 'Student'),
    #     (TEACHER, 'Teacher'),
    #     (SUPERVISOR, 'Supervisor'),
    # )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    #role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username


# 이제 signals 을 정의하여 User 객체가 생성되고 수정될 때 관련된 Profile Model 또한 자동으로 생성되고
# 업데이트 되도록 할 것입니다. post_save signal 이라는 것을 사용하는 것인데,
# sender=User 설정에 의해서 User의 save() 가 호출될 때마다 그 직후에 create_user_profile, save_user_profile 이 호출됩니다.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()
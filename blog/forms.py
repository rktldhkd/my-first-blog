# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment

#CRUD 에서 Read는 views 에서 쉘 명령어로 그냥 불러오는게 가능.
#R을 제외한 CUD는 따로 클래스를 만들어서 처리하는 편.

#장고에 이 폼이 ModelForm이라는 것을 알려줘야해요. (그러면 장고가 뭔가 마술을 부릴 거에요)
# - forms.ModelForm은 ModelForm이라는 것을 알려주는 구문이에요.
class PostForm(forms.ModelForm):

    # class Meta가 나오는데요, 이 폼을 만들기 위해서 어떤 model이 쓰여야 하는지 장고에 알려주는 구문입니다. (model = Post).
    class Meta:
        model   = Post
        #마지막으로, 이 폼에 필드를 넣으면 완성되겠죠. 이번 폼에서는 title과 text만 보여지게 해 봅시다.
        # - author는 현재 로그인 하고 있는 사람이 될 것이고 (바로 당신이요!) 그리고 created_date는 글이
        # 등록되는 시간이 될 것입니다. (예를 들어, 코드 상에서요), 됐죠?
        fields  = ('title', 'file', 'photo', 'text',)

    # init 함수에서 self.fields['file'].required = False 설정을 통해 file 값이 없더라도
    # view에서 유효성 검사에서 오류를 발생시키지 않도록 해준다.
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['photo'].required = False
        self.fields['file'].required = False


#로그인 폼
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '아이디',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '비밀번호',
            }
        )
    )

#댓글 폼
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text', 'created_date')
        widgets = {
            'author': forms.TextInput(attrs={
                                        'class': 'form-control',
                                        'readonly': 'readonly',
                                    }),
            'text': forms.Textarea(attrs={
                                        'class': 'form-control',
                                        'placeholder': '댓글을 입력하세요.'
                                    }),
            'created_date': forms.DateInput(format='%Y-%m-%d %H:%M:%S', attrs={
                                        'class': 'form-control',
                                        'readonly': 'readonly',
                                    }),

        }


#회원가입 폼
class SignUpForm(UserCreationForm):
    #This form won’t save automatically the birth_date on form.save(). Instead, we have to handle it manually:
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'birth_date', 'password1', 'password2',)
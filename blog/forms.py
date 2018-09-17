from django import forms
from .models import Post

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
        fields  = ('title', 'text',)
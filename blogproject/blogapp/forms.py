from django import forms
from django.core.exceptions import ValidationError
from re import match
import re
from argon2 import PasswordHasher
from .models import User, Post

class RegistrationForm(forms.Form):
    user_name = forms.CharField(max_length=50)
    user_id = forms.CharField(max_length=100)
    user_pw = forms.CharField(max_length=100, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    user_email = forms.EmailField(max_length=100)

    def clean_user_id(self):
        clean_user_id = super().clean().get('user_id')
        if User.objects.filter(user_id=clean_user_id).exists():
            raise forms.ValidationError('이미 존재하는 ID입니다.')
        return clean_user_id

    def clean_email(self):
        clean_email = self.cleaned_data.get('user_email')
        # 이메일 유효성 검사 규칙을 여기에 추가
        regex_email = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(regex_email, clean_email):
            raise ValidationError('유효하지 않은 이메일 주소입니다.')
        return clean_email

    def clean(self):
        cleaned_data = super().clean()
        user_pw = cleaned_data.get("user_pw")
        confirm_password = cleaned_data.get("confirm_password")
        regex_password = '^(?=.*[a-z])(?=.*\d).{8,}$'
        if not re.match(regex_password, user_pw):
            raise ValidationError('소문자 하나가 포함된 8~25자리 비밀번호를 입력해주세요.')
            
        if user_pw != confirm_password:
            raise ValidationError("비밀번호와 비밀번호 확인이 일치하지 않습니다.")

        

class CustomLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'User_id', 'class': 'login-input'}),
        label='',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'login-input'}),
        label='',
    )

# 이 부분은 강사님 코드 복붙해온 부분
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].required = False
        self.fields['publish'].required = False
        self.fields['views'].required = False  
    
    
    

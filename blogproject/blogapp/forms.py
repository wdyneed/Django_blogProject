from django import forms
from django.core.exceptions import ValidationError
from re import match
import re
from argon2 import PasswordHasher
from .models import User

class RegistrationForm(forms.Form):
    user_name = forms.CharField(max_length=50)
    user_id = forms.CharField(max_length=100)
    user_pw = forms.CharField(max_length=100, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    user_email = forms.EmailField(max_length=100)
    
   # 이미 존재하는 아이디면 회원가입을 막아야하는데 존재하는 아이디임에도 불구하고 회원가입이 되어버림
    def clean_userid(self):
        userid = super().clean().get('user_id')
        if User.objects.get(user_id=userid) == True:
            raise ValidationError('이미 존재하는 ID입니다.')
        return userid

    def clean_email(self):
        email = self.cleaned_data.get('user_email')
        # 이메일 유효성 검사 규칙을 여기에 추가
        regex_email = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(regex_email, email):
            raise ValidationError('유효하지 않은 이메일 주소입니다.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        user_pw = cleaned_data.get("user_pw")
        confirm_password = cleaned_data.get("confirm_password")
        regex_password = '^(?=.*[a-z])(?=.*\d).{8,}$'
        if not re.match(regex_password, user_pw):
            raise ValidationError('소문자 하나가 포함된 8~25자리 비밀번호를 입력해주세요.')
            
        if user_pw != confirm_password:
            raise ValidationError("비밀번호와 비밀번호 확인이 일치하지 않습니다.")

        
class LoginForm(forms.Form):                                  
    user_id = forms.CharField(                             
        error_messages={                                     
            'required': '아이디를 입력해주세요'
        },
        max_length=32, label="사용자이름")                    
    
    user_pw = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput, label="비밀번호")       
    
    def clean(self):                                        
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        user_pw = cleaned_data.get('user_pw')

        if user_id and user_pw :
            try:
                user = User.objects.get(user_id=user_id)
                if not PasswordHasher().verify(user_pw, user.user_pw):
                    self.add_error('user_pw', '비밀번호를 틀렸습니다.')    
                else:
                    self.user_id = user.user_id                             
            except Exception:
                self.add_error('user_id', '존재하지 않는 아이디 입니다.')
    

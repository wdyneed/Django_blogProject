from django import forms
from django.core.exceptions import ValidationError
from re import match
import re
from argon2 import PasswordHasher

class RegistrationForm(forms.Form):
    user_name = forms.CharField(max_length=50)
    user_id = forms.CharField(max_length=100)
    user_pw = forms.CharField(max_length=100, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    user_email = forms.EmailField(max_length=100)

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
    
    
    

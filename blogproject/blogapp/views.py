from rest_framework import viewsets
from .models import Post, User
from .serializers import PostSerializer
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from argon2 import PasswordHasher

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            user_id = form.cleaned_data['user_id']
            user_pw = PasswordHasher().hash(form.cleaned_data['user_pw'])
            user_email = form.cleaned_data['user_email']
            # 이 부분에서 User 모델을 생성하고 데이터베이스에 저장합니다.
            user = User(user_name=user_name, user_id=user_id, user_pw=user_pw, user_email=user_email)
            user.save()
            return redirect('/')  # 회원가입 성공 페이지로 이동
    else:
        form = RegistrationForm()
    
    return render(request, './register.html', {'form': form})


def custom_login(request):
    if request.method =="POST":
        form = LoginForm(request.POST)                         
        if form.is_valid():                                      
            request.session['user'] = form.user_id               
            return redirect('/')
    else:
        form = LoginForm()                                        
    
    return render(request, 'login.html', {'form': form}) 


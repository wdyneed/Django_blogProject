from rest_framework import viewsets
from .models import Post, User
from .serializers import PostSerializer
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import RegistrationForm
from django.core.exceptions import ValidationError
from argon2 import PasswordHasher
from django.contrib import messages
from .forms import CustomLoginForm
from django.contrib.auth import authenticate, login, logout

# Post 시리얼라이저인데 이 부분은 아래 index랑 비슷한 역할을 함 하지만 시리얼라이저로 구현할지 고민중
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# 로그인 하는 곳 (아직 미구현)
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CustomLoginForm(data=request.POST or None)  # 커스텀 로그인 폼 사용
        if request.method == "POST":
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')  # 슈퍼유저와 일반 사용자 모두 동일한 페이지로 리다이렉션
        return render(request, 'login.html', {'form': form})                                      
    
    
def custom_logout(request):
    if request.method == 'GET':
        logout(request)
        return redirect('/login/')
    return redirect('/login/')
    
    
# 인덱스 화면 불러오는 함수
def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts' : posts})


def add_Post_data(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        published_date = request.POST["published_date"]

        post = Post(title=title, content=content, published_date=published_date)
        post.save()
        return redirect("site")

    return render(request, "blogapp/site.html")

# 게시글 누르면 보는 테스트용 view(미완성)
def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'site2.html', {'post': post})
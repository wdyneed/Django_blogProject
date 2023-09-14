from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from django.shortcuts import render, redirect, get_object_or_404
from argon2 import PasswordHasher
from .forms import CustomLoginForm, PostForm
from django.contrib.auth import authenticate, login, logout
from bs4 import BeautifulSoup
from django.core.paginator import Paginator
from django.conf import settings
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views import View
from django.core.files.storage import default_storage
from django.conf import settings
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
        return redirect('/')
    return redirect('/')
    
    
# 인덱스 화면 불러오는 함수
def index(request):
    representpost = Post.objects.filter(publish='Y').order_by('-view_count').first()
    posts = Post.objects.all().order_by('published_date').exclude(id=representpost.id)
    posts_per_page = 6
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    return render(request, 'index.html', {'posts' : posts, 'representpost' : representpost, 'page_posts': page_posts})

# 글 작성하는 함수
def board_write(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # request.FILES를 사용하여 이미지 처리
        print(form)
        if form.is_valid():
            # 폼 데이터를 모델에 저장
            form = form.save(commit=False)
            form.writer = request.user  # 현재 로그인한 사용자를 작성자로 설정
            form.save()
            return redirect('/')  # 성공 시 홈 페이지로 리디렉션
    else:
        form = PostForm()
    return render(request, 'site.html', {'form': form})


def view_post(request, post_id):
    # 포스트 id로 게시물 가져옴
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST': 

        # 요청에 삭제가 포함된경우
        if 'delete-button' in request.POST:
            post.delete()
            return redirect('/')

    # 조회수 증가 및 db에 저장
    post.view_count += 1
    post.save()
    # 이전/다음 게시물 가져옴
    previous_post = Post.objects.filter(id__lt=post.id, publish='Y').order_by('-id').first()
    next_post = Post.objects.filter(id__gt=post.id, publish='Y').order_by('id').first()

    # 같은 주제인 게시물들 중 최신 글 가져옴
    recommended_posts = Post.objects.filter(topic=post.topic, publish='Y').order_by('-published_date')[:2]
    # 게시물 내용에서 첫번째 이미지(썸네일) 태그 추출
    for recommended_post in recommended_posts:
        soup = BeautifulSoup(recommended_post.content, 'html.parser')
        image_tag = soup.find('img')
        recommended_post.image_tag = str(image_tag) if image_tag else ''
    
    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'recommended_posts': recommended_posts,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'site_2.html', context)

class image_upload(View):
    
    # 사용자가 이미지 업로드 하는경우 실행
    def post(self, request):
        
        # file필드 사용해 요청에서 업로드한 파일 가져옴
        file = request.FILES['file']
        
        # 저장 경로 생성
        filepath = 'uploads/' + file.name
        
        # 파일 저장
        filename = default_storage.save(filepath, file)
        
        # 파일 URL 생성
        file_url = settings.MEDIA_URL + filename
        
        # 이미지 업로드 완료시 JSON 응답으로 이미지 파일의 url 반환
        return JsonResponse({'location': file_url})
    
# def create_or_update_post(request, post_id=None):
#     # 글수정 페이지의 경우
#     if post_id:
#         post = get_object_or_404(Post, id=post_id)
    
#     # 글쓰기 페이지의 경우, 임시저장한 글이 있는지 검색 
#     else:
#         post = Post.objects.filter(author_id=request.user.username, publish='N').order_by('-created_at').first()

#     # 업로드/수정 버튼 눌렀을 떄
#     if request.method == 'POST':
#         form = PostForm(request.POST, instance=post) # 폼 초기화
#         if form.is_valid():
#             post = form.save(commit=False)

#             # 게시물 삭제
#             if 'delete-button' in request.POST:
#                 post.delete() 
#                 return redirect('blog_app:site') 

#             if not form.cleaned_data.get('topic'):
#                 post.topic = '전체'
            
#             # 임시저장 여부 설정
#             if 'temp-save-button' in request.POST:
#                 post.publish = 'N'
#             else:
#                 post.publish = 'Y'

#             # 글쓴이 설정
#             post.author_id = request.user.username

#             post.save()
#             return redirect('blog_app:view_post', post_id=post.id) # 업로드/수정한 페이지로 리다이렉트
    
#     # 수정할 게시물 정보를 가지고 있는 객체를 사용해 폼을 초기화함
#     else:
#         form = BlogPostForm(instance=post)

#     template = 'blog_app/write.html'
#     context = {'form': form, 'post': post, 'edit_mode': post_id is not None, 'MEDIA_URL': settings.MEDIA_URL,} #edit_mode: 글 수정 모드여부

#     return render(request, template, context)


def calculate_format_datetime(published_date):
    current_datetime = datetime.now()
    time_difference = current_datetime - published_date

    if time_difference.days > 0:
        # 날짜 차이가 1일 이상인 경우
        return published_date.strftime("%Y-%m-%d %H:%M")
    elif time_difference.seconds >= 3600:
        # 1시간 이상 24시간 미만인 경우
        hours = time_difference.seconds // 3600
        return f"{hours}시간 전"
    elif time_difference.seconds >= 60:
        # 1분 이상 1시간 미만인 경우
        minutes = time_difference.seconds // 60
        return f"{minutes}분 전"
    else:
        # 1분 미만인 경우
        return "방금 전"
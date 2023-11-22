from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from django.shortcuts import render, redirect, get_object_or_404
from argon2 import PasswordHasher
from .forms import CustomLoginForm, PostForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.core.files.storage import default_storage
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm
import openai


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

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
def index(request, topic=None):
    sort = request.GET.get('sort', '')
    posts = Post.objects.filter(publish='Y')
    if topic:
        representpost = Post.objects.filter(topic=topic, publish='Y').order_by('-view_count').first()
        posts = posts.filter(topic=topic)
        if representpost:
            if sort == 'views':
                posts = posts.order_by('-view_count')
            else:
                 posts = posts.order_by('-published_date')
        else:
            pass
        posts_per_page = 6
        paginator = Paginator(posts, posts_per_page)
        page_number = request.GET.get('page')
        page_posts = paginator.get_page(page_number)
        return render(request, 'index.html', {'posts' : posts, 'representpost' : representpost, 'page_posts': page_posts, 'sort' : sort})
    
    else:
        representpost = Post.objects.filter(publish='Y').order_by('-view_count').first()
        if representpost:
            if sort == 'views':
                posts = posts.order_by('-view_count')
            else:
                 posts = posts.order_by('-published_date')
            pass
        posts_per_page = 6
        paginator = Paginator(posts, posts_per_page)
        page_number = request.GET.get('page')
        page_posts = paginator.get_page(page_number)
        return render(request, 'index.html', {'posts' : posts, 'representpost' : representpost, 'page_posts': page_posts, 'sort' : sort})


# 글 작성하는 함수
def board_write(request):
    selected_post = None
    if request.method == 'POST':
        form = PostForm(request.POST, instance=selected_post)  # request.FILES를 사용하여 이미지 처리
        if form.is_valid():
            post = form.save(commit=False)
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            topic = form.cleaned_data['topic']
            post = Post(title=title, content=content, topic=topic)
            if 'temp-save-button' in request.POST:
                post.publish = 'N'
            else:
                post.publish = 'Y' 
            post.save()
            return redirect('blogapp:view_post', post_id = post.id)  # 성공 시 홈 페이지로 리디렉션
    else:
        form = PostForm(instance=selected_post)
    return render(request, 'write.html', {'form': form, 'post' : selected_post})


def view_post(request, post_id):
    # 포스트 id로 게시물 가져옴
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST': 

        # 요청에 삭제가 포함된경우
        if 'delete-button' in request.POST:
            post.delete()
            return redirect('/')

    # 조회수 증가 및 db에 저장

    if 'post_viewed_%s' % post_id not in request.session:
        post.view_count += 1
        post.save()
        request.session['post_viewed_%s' % post_id] = True
    
    
    # 이전/다음 게시물 가져옴
    previous_post = Post.objects.filter(id__lt=post.id, publish='Y').order_by('-id').first()
    next_post = Post.objects.filter(id__gt=post.id, publish='Y').order_by('id').first()

    # 같은 주제인 게시물들 중 최신 글 가져옴
    recommended_posts = Post.objects.filter(topic=post.topic, publish='Y').exclude(id=post.id).order_by('?')[:2]
    
    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'recommended_posts': recommended_posts,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'post.html', context)

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
    
#게시물 수정,삭제
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return JsonResponse({'message': '게시물이 삭제되었습니다.'})
    
def edit_post(request, post_id):
    # 해당 post_id에 해당하는 포스트를 가져옵니다.
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            # 수정이 완료되면 홈페이지('/')로 리다이렉트합니다.
            return redirect('blogapp:view_post', post_id = post.id)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
    }

    return render(request, 'edit_post.html', context)


def autocomplete(request):
    openai.api_key = settings.API_KEY
    if request.method == "POST":

        #제목 필드값 가져옴
        prompt = request.POST.get('title')
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            # 반환된 응답에서 텍스트 추출해 변수에 저장
            message = response['choices'][0]['message']['content']
        except Exception as e:
            message = str(e)
        return JsonResponse({"message": message})
    return render(request, 'autocomplete.html')

def temp_save(request):
    posts = Post.objects.filter(publish='N').order_by('-published_date')
    return render(request, 'popup.html', {'posts' : posts})
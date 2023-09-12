from django.db import models

# Create your models here.


# 글 게시(글제목, 내용(+사진), 게시 날짜, 태그정보, 게시한 유저id)
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="글 제목")
    content = models.TextField(verbose_name="글 내용")
    published_date = models.DateTimeField(verbose_name="업로드 날짜")


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post/%Y/%m/%d")


# 회원가입 (id, 비밀번호, 이름, 이메일)
class User(models.Model):
    user_id = models.CharField(max_length=50, verbose_name="유저 아이디", unique=True, primary_key=True)
    user_pw = models.CharField(max_length=300, verbose_name="유저 비밀번호")
    user_name = models.CharField(max_length=20, verbose_name="유저 이름")
    user_email = models.EmailField(max_length=100, verbose_name="유저 이메일")

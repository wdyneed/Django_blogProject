from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.


# 글 게시(글제목, 내용(+사진), 게시 날짜, 태그정보, 게시한 유저id)
class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="태그 이름")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일자")

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="카테고리 이름")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일자")

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="글 제목")
    content = models.TextField(verbose_name="글 내용")
    published_date = models.DateTimeField(verbose_name="업로드 날짜")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자", default=1)
    tags = models.ManyToManyField(Tag, verbose_name="태그", blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="카테고리", blank=True, null=True
    )
    text = RichTextField()

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post/%Y/%m/%d")

from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="글 제목")
    content = RichTextField()
    published_date = models.DateTimeField(verbose_name="업로드 날짜", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자", default=1)
    topic = models.CharField(max_length=255, default='전체')
    view_count = models.PositiveIntegerField(default=0, verbose_name='조회수')
    publish = models.CharField(max_length=1, default='Y')
    image = models.ImageField(null=True, upload_to="", blank = True)

    def __str__(self):
        return self.title

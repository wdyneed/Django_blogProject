from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, image_upload
from blogapp.views import image_upload
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'posts', PostViewSet)
app_name = 'blog_app'
urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', views.custom_login, name='login'),
    path('', views.index, name='site'),
    path('logout/', views.custom_logout, name='logout'),
    path('posting/',views.board_write, name='posting'),
    path('post/<int:post_id>/', views.view_post, name='view_post'),
    path('upload/', image_upload.as_view(), name='image_upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
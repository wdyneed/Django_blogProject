from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', views.custom_login, name='login'),
    path('', views.index, name='site'),
    path('logout/', views.custom_logout, name='logout'),
    path('posting/',views.add_Post_data, name='posting'),
    path('post/<int:post_id>/', views.view_post, name='view_post')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
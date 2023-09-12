from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet
from . import views

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('', views.index, name='site'),
]
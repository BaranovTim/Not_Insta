from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import views
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .views import PostViewSet
from .views import index, post, login_view, post_edit, like_post


r = DefaultRouter()
r.register(r'posts', PostViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('post/', views.post, name='post'),
    path('post/<int:post_id>/edit/', post_edit, name='post_edit'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('login/', login_view, name='login'),
] + r.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

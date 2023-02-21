from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('retry/', views.retry_outline, name='retry'),
    path('blog-post/', views.blogpost, name='blogpost'),
    path('rewrite-blogpost/', views.rewrite_post, name='rewrite_post'),
    #path('rewrite-blog-post/', views.rewrite_blogpost, name='rewrite_blogpost'),
    path('meta-description/', views.meta_description, name='meta'),
    path('youtube-links/', views.youtube_link, name='youtube_link'),
    path('get/', views.get_youtube_link, name='get_youtube_link'),
    path('add-youtube-link/', views.add_youtube_link, name='add_youtube'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html'
        ),
         name='login'
        ),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='logout.html'
        ),
         name='logout'
        ),
]

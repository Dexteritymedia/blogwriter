from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog-post/', views.blogpost, name='blogpost'),
    path('meta-description/', views.meta_description, name='meta'),
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

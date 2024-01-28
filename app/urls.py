from django.urls import path
from . import views

urlpatterns = [
    path('',views.homePage,name="home"),
    path('register/', views.register_user, name="register_user"),
    path('login/', views.login_user, name="login_user"),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('edit/<slug:slug>/', views.edit_post, name='edit_post'),
]
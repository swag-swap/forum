from django.urls import path
from . import views 
 

urlpatterns = [
    path('',views.homePage,name="home"),
    path('register/', views.register_user, name="register_user"),
    path('login/', views.login_user, name="login_user"),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('edit/<slug:slug>/', views.edit_post, name='edit_post'),
    path('create/', views.create_post, name='create_post'),
    path('logout/', views.my_logout, name='logout'),
    path('delete-post/<slug:slug>/', views.delete_post, name='delete_post'),
    path('searched-post/<slug:slug>/',views.search_posts, name='search_posts'),
]
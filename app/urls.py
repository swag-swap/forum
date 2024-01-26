from django.urls import path
from . import views

urlpatterns = [
    path('',views.homePage,name="homePage"),
    path('register/', views.register_user, name="register_user")
]
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('',views.home_view, name="home"),
    path('register/', views.register_user, name="register_user"),
    path('login/', views.login_user, name="login_user"),
    path('logout/', views.my_logout, name='logout'),
    path('admin/', admin.site.urls),
    path('post/', include("postApp.urls"), name="post"),
    path('test/', include("testApp.urls"), name="test"), 
    path("ckeditor5/", include('django_ckeditor_5.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
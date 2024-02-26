from django.urls import path
from . import views 
 

urlpatterns = [ 
    path('',views.test_home, name='test_home'),
    path('create/', views.create_test, name='create_test'), 
    path('<slug:slug>/', views.test_detail, name='test_detail'),
    path('edit/<slug:slug>/', views.edit_test, name='edit_test'),
    path('delete-test/<slug:slug>/', views.delete_test, name='delete_test'),
    path('searched-test/<slug:slug>/',views.search_test, name='search_test'),
]
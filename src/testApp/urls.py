from django.urls import path
from . import views 
 

urlpatterns = [ 
    path('',views.test_list, name='tests'),
    path('create/', views.test_create, name='test_create'), 
    path('<int:slug>/', views.test_detail, name='test_detail'),
    path('edit/<int:slug>/', views.test_manage_detail, name='manage_test'),
    # path('delete-test/<slug:slug>/', views.delete_test, name='delete_test'),
    # path('searched-test/<slug:slug>/',views.search_test, name='search_test'),
    # path('add_question/<int:test_id>/', views.add_question, name='add_question'), 

]
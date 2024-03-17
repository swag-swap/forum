from django.urls import path
from . import views 
 

urlpatterns = [ 
    path('',views.test_list, name='tests'),
    path('create/', views.test_create, name='create_test'), 
    path('edit/<int:slug>/', views.test_manage_detail, name='manage_test'),  
    path('delete-test/<slug:slug>/', views.delete_test, name='delete_test'),
    path('update-test/<slug:slug>/', views.update_test, name='update-test'),
    # path('get/<int:slug>/', views.test_questions_options, name='test_questions_options'),
    # path('searched-test/<slug:slug>/',views.search_test, name='search_test'),
    # path('add_question/<int:test_id>/', views.add_question, name='add_question'), 
    # path('<int:slug>/', views.test_detail, name='test_detail'),

]
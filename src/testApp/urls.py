from django.urls import path
from . import views 
 

urlpatterns = [ 
    path('',views.test_list, name='tests'),
    path('create/', views.test_create, name='create_test'), 
    path('edit/<int:slug>/', views.test_manage_detail, name='manage_test'),  
    path('delete-test/<slug:slug>/', views.delete_test, name='delete_test'),
    path('get-test-data/<slug:slug>/', views.get_test_data, name='get-test-data'),
    path('get-question/<int:id>/', views.get_question, name='get_question'),  
    path('update-test-questions/<int:slug>/', views.update_test_questions, name='update_test_questions'),
    path('add-question/<int:slug>/', views.add_question, name='add_question'), 
    path('give-test/<int:slug>',views.give_test, name='give_test'),
    path('<int:slug>/', views.test_detail, name='test_detail'),
    path('submit-test/<int:slug>',views.submit_test, name='submit_test'),
    path('view-score/<int:slug>/', views.view_score, name='view_score'),
    # path('searched-test/<slug:slug>/',views.search_test, name='search_test'),

]
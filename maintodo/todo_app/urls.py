from django.urls import path
from django.contrib.auth.views import PasswordChangeView
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('list/<int:list_id>/', views.list, name='list'),
    path('lists/', views.user_to_dolist, name='lists'),
    path('add_list/', views.add_list, name='add_list'),
    path('list/<int:list_id>/', views.user_to_dolist, name='list'),
    path('list/<int:list_id>/add_task/', views.add_task, name='add_task'),

    path('list/complete/<int:task_id>/', views.complete_task, name='complete_task'),

    path('list/deletetask/<int:task_id>/', views.delete_task, name='delete_task'),
    path('list/deletelist/<int:list_id>/', views.delete_list, name='delete_list'),

    path('change_password/', views.change_password, name='change_password'),



    path('user_list/', views.user_list, name='user_list'),
    path('user_lists/', views.user_lists, name='user_lists'),
]

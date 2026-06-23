# qa/urls.py

from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'ask/',
        views.ask_question,
        name='ask_question'
    ),

    path(
        'question/<int:pk>/',
        views.question_detail,
        name='question_detail'
    ),

    path(
        'profile/<int:user_id>/',
        views.profile,
        name='profile'
    ),

    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('question/edit/<int:pk>/', views.edit_question, name='edit_question'),
    path('question/delete/<int:pk>/', views.delete_question, name='delete_question'),

    path(
       'user/<int:user_id>/',
        views.user_profile,
        name='user_profile'
    ),

    path(
        'answer/edit/<int:answer_id>/',
        views.edit_answer,
        name='edit_answer'
    ),

    path(
        'answer/delete/<int:answer_id>/',
        views.delete_answer,
        name='delete_answer'
    ),
    
    path(
        'answer/accept/<int:answer_id>/',
        views.accept_answer,
        name='accept_answer'
    ),

    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),

    path(
        'followers/<int:user_id>/',
        views.followers_list,
        name='followers_list'
    ),

    path(
        'ajax/followers/<int:user_id>/',
         views.followers_modal,
         name='followers_modal'
    ),
    
    path('ajax/following/<int:user_id>/', views.ajax_following, name='ajax_following'),
]



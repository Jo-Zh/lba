from django.urls import path
from . import views

urlpatterns=[
    path('', views.home),
    path('home', views.home, name='home'),
    path('home/<slug:slug>', views.home, name='home_category'),
    path('sign-up-reader', views.sign_up_reader),
    path('sign-up-poster', views.sign_up_poster),
    path('user-profile/<int:id>/', views.user_profile, name='userprofile'),
    path('user-profile-update/<int:pk>/', views.ProfileUpdateView.as_view(), name='update-profile'),
    path('user-delete/<int:id>/', views.user_delete, name='delete-profile'),
    path('user-passwordreset/<int:id>/', views.password_update, name='update-password'),

    path('detail/<int:id>/', views.article_detail, name='detail'),
    path('newpost/<int:id>/', views.new_post, name='newpost'),
    path('post-status/<int:id>/', views.article_status, name='post-status'),
    path('updatepost/<int:pk>/', views.PostUpdateView.as_view(), name='updatepost'),
    path('home/favor/<int:id>', views.add_favorite, name='addfavor'),
    path('post-delete/<int:id>/', views.post_delete, name='delete-post'),

    path('note-delete/<int:id>/', views.note_delete, name='note-delete')
 
]
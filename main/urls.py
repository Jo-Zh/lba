from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up-reader', views.sign_up_reader),
    path('sign-up-poster', views.sign_up_poster),
    path('<int:id>/user-profile', views.user_profile, name='userprofile'),
    path('<int:id>/user-update', views.user_update, name='update-profile'),
    path('<int:id>/user-delete', views.user_delete, name='delete-profile'),


    path('<int:id>/detail', views.article_detail, name='detail'),
    # path('<int:id>/posts', views.user_posts, name='posts'),
    path('<int:id>/newpost', views.new_post, name='newpost'),
    path('home/favor/<int:id>', views.add_favorite, name='addfavor'),
    path('<int:id>/post-delete', views.post_delete, name='delete-post'),
 
]
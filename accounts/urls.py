# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create_article/', views.create_article, name='create_article'),
    path('edit_article/<int:article_id>/', views.edit_article, name='edit_article'),
    path('delete_article/<int:article_id>/', views.delete_article, name='delete_article'),
    # Define URLs for user profiles as needed
]

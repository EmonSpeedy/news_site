from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('category/<slug:category_slug>/', views.articles_by_category, name = 'articles_by_category'),
    path('article/<int:article_id>/', views.article_detail, name = 'article_detail'),
    path('rate/<int:article_id>/', views.rate_article, name = 'rate_article'),
]
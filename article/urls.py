from django.urls import path
from .views import (
                    ArticleView,
                    ArticleDetailView,
                    AuthorArticlesView,
                    ArticleTagView,
                    
)

app_name = 'article'

urlpatterns = [
    path('', ArticleView.as_view(), name='articles'),
    path('<str:slug>/', ArticleDetailView.as_view(), name='article-details'),
    path('author/<str:username>/', AuthorArticlesView.as_view(), name='author_articles'),
    path('tag/<str:tagname>/', ArticleTagView.as_view(), name='article-tag'),

]
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Article,Category,ArticleTag
from .forms import CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
class ArticleView(generic.ListView):
    model = Article
    template_name = 'article/article_list.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self):
        qs = self.model.published.all().order_by('-created_at')
        search = self.request.GET.get('q')
        category = self.request.GET.get('category')
        tag_filter = self.request.GET.get('article_tag', None)

        if search:
            qs = qs.filter(Q(title__icontains=search))
        if category:
            qs = qs.filter(category__slug=category)
        if tag_filter:
            article_tag = ArticleTag.objects.filter(Q(slug=tag_filter)).first()
            if article_tag:
                article_tag.increment_views()
                qs = qs.filter(tags=article_tag)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top_articles_tags"] = ArticleTag.objects.all().order_by('-views')[:20]

        return context
class ArticleDetailView(generic.View):
    model = Article
    template_name = 'article/article_detail.html'
    form_class = CommentForm

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        comments = article.comments.filter(active=True)
        comment_form = self.form_class()  # Initialize an empty CommentForm

        return self.render_with_context(request, article, comments, comment_form)

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        comments = article.comments.filter(active=True)
        comment_form = self.form_class(request.POST)
        new_comment = None

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
            comment_form = self.form_class()  # Initialize an empty CommentForm after submission

        return self.render_with_context(request, article, comments, comment_form, new_comment)

    def render_with_context(self, request, article, comments, comment_form, new_comment=None):
        context = self.get_context_data(article, comments, comment_form, new_comment)
        # Loop through comments to check for replies

        return render(request, self.template_name, context)

    def get_context_data(self, article, comments, comment_form, new_comment=None):
        context = {
            'article': article,
            'comments': comments,
            'comment_form': comment_form,
            'top_article_tags': ArticleTag.objects.all().order_by('-views')[:20],
            'top_articles': Article.published.all().order_by('-views')[:4],
            'top_categories': Category.objects.all().order_by('-views'),
            'last_articles': Article.published.all().order_by('-created_at')[:10],

            'articles_count': Article.published.count(),
            # 'comment_count': ArticleComment.published.count(),

        }
        if new_comment is not None:
            context['new_comment'] = new_comment
        return context


class AuthorArticlesView(generic.ListView):
    model = Article
    template_name = 'article/article_list.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_username = self.kwargs.get('username')
        author = get_object_or_404(User, username=author_username)
        context['author'] = author
        return context

    def get_queryset(self):
        qs = self.model.published.all().order_by('-created_at')
        author_username = self.kwargs.get('username')

        if author_username:
            author = get_object_or_404(User, username=author_username)
            qs = qs.filter(author=author)

        return qs


class ArticleTagView(generic.ListView):
    model = Article
    template_name = 'article/articles.html'
    context_object_name = 'articles'
    paginate_by = 12
    page_name = "بلاگ"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_name"] = self.page_name
        context["top_articles"] = self.get_queryset().order_by('-views')[:4]
        context["articles_count"] = self.get_queryset().count()
        context["top_articles_tags"] = ArticleTag.objects.all().order_by('-views')[:20]
        context["article_tags"] = ArticleTag.objects.all()  # Fetch all article tags

        tag_name = self.kwargs.get('tagname')
        filtered_tag = ArticleTag.objects.filter(slug=tag_name).first()
        if filtered_tag:
            filtered_tag.increment_views()
            context["filtered_tag"] = filtered_tag

        return context

    def get_queryset(self):
        queryset = self.model.published.all()

        # Get the tagname from URL parameters
        tag_name = self.kwargs.get('tagname')

        # Filter ArticleTag based on the tagname
        filtered_tag = ArticleTag.objects.filter(slug=tag_name).first()

        if filtered_tag:
            # If the tag exists, increment its views
            filtered_tag.increment_views()
            # Filter articles based on the filtered tag
            queryset = queryset.filter(tags=filtered_tag)

        return queryset
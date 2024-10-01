from django.contrib import admin

# Register your models here.
from .models import Article, Category,ArticleTag


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_created_at', 'get_updated_at', \
        'views', 'publish', 'reed_time')
    list_filter = ('publish', 'created_at')
    readonly_fields = ('reed_time', 'slug')
    search_fields = ('title', 'body', 'id')
    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'views', 'slug')
    search_fields = ('title', )

@admin.register(ArticleTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('title', 'views', 'slug')
    search_fields = ('title', )



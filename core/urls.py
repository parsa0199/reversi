""" core URL Configuration """

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import sitemaps
from django.contrib.sitemaps.views import sitemap
from .sitemaps.sitemaps import *
from .sitemaps.views import *
# sitemaps = {
#     'posts': ArticleSitemap,
#     'products': ProductSitemap,
# }

urlpatterns = [


    path('admin/', admin.site.urls),


    
    path('ckeditor/', include('ckeditor_uploader.urls')),


    # Main urls
    path('', include('main.urls', namespace='main')),

    # Dashboard urls
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    # article urls
    path('blog/', include('article.urls', namespace='article')),
    # game urls
    path('game/', include('game.urls')),

]

handler404 = 'main.views.handler404'

# Development
if bool(settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
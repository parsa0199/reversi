from django.http import HttpResponse
import os
from django.shortcuts import render


if os.getenv('DB_ENGINE', 'postgres'):
    domain = "https://balckdesigner.ir"
else:
    domain = "http://localhost:8000"


def master_sitemap(request):
    sitemap_urls = [
        request.build_absolute_uri('/post-sitemap.xml'),
        request.build_absolute_uri('/product-sitemap.xml'),
        request.build_absolute_uri('/product_cat-sitemap.xml'),
        request.build_absolute_uri('/product_tag-sitemap.xml'),
        request.build_absolute_uri('/author-sitemap.xml'),
    ]
    return render(request, 'includes/master_sitemap.xml', {'sitemap_urls': sitemap_urls}, content_type='application/xml')
# main/context_processors.py

from .models import SiteInfo

def site_info(request):
    try:
        site_info = SiteInfo.objects.latest('created_at')
    except SiteInfo.DoesNotExist:
        site_info = None

    return {
        'site_info': site_info
    }

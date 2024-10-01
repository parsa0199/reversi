from django.contrib import admin
from .models import SiteInfo

@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_created_at', 'get_updated_at', 'phone', 'email')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'phone', 'email', 'address', 'meta_title')
    readonly_fields = ('get_created_at', 'get_updated_at')

    fieldsets = (
        (None, {
            'fields': ('name', 'logo', 'description')
        }),
        ('اطلاعات تماس', {
            'fields': ('phone', 'email', 'address')
        }),
        ('اطلاعات سئو', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('لینک‌های شبکه اجتماعی', {
            'fields': ('facebook', 'twitter', 'instagram', 'linkedin', 'youtube')
        }),
        ('تاریخ‌ها', {
            'fields': ('get_created_at', 'get_updated_at')
        }),
    )

    def has_add_permission(self, request, obj=None):
        """Limit to one instance of site info"""
        return not SiteInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of site info"""
        return False

from django.contrib import admin
from .models import ContactMessage, SmsLog


class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]


    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
# --------------------------------------------
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'get_created_at', 'status')
    readonly_fields = ('status',)
    actions = ['mark_as_seen']

    def mark_as_seen(self, request, queryset):
        queryset.update(status='seen')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.model.objects.get(pk=object_id)
        if obj.status == 'not_seen':
            obj.status = 'seen'
            obj.save()
        return super().change_view(request, object_id, form_url, extra_context)

admin.site.register(ContactMessage, ContactMessageAdmin)

@admin.register(SmsLog)
class SmsLogAdmin(ReadOnlyAdmin):
    list_display = ('user', 'subject', 'is_sent', 'status_code', 'get_created_at')
    list_filter = ('user', 'subject', 'is_sent', 'status_code', 'created_at')
    ordering = ('-created_at', )
    # readonly_fields = ('status_code_str', )




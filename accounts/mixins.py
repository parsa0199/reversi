from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect, render

# Only superusers
class AdminAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_superuser:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


# Only users that verify their phone number and email address
class UserVerificationMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not (user.valid_phone and user.valid_email):
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)


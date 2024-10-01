from django.db.models.aggregates import Sum, Count
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from .models import *
from accounts.models import *
from accounts.mixins import *
from django.db.models import Q, Count
from django.http import HttpResponse
from jalali_date import datetime2jalali, date2jalali
from datetime import datetime, timedelta
import csv, xlwt
import pandas as pd
from django.contrib import messages

from main.models import ContactMessage
from site_info.models import SiteInfo


# --------------------------------- Home View ---------------------------------
class HomeView(LoginRequiredMixin, AdminAccessMixin, generic.TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        today = datetime.today().date()
        context = super().get_context_data(**kwargs)
        context["customers_count"] = User.objects.count()

        return context



# --------------------------------messages views--------------------------------------
class MessagesView(LoginRequiredMixin, AdminAccessMixin, generic.ListView):
    model = ContactMessage
    template_name = 'dashboard/messages/messages.html'
    context_object_name = 'contact_messages'
    paginate_by = 50

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context["object_name_fa"] = 'پیام'
        context["object_name_fa_plural"] = 'پیام ها'
        context['objects_count'] = self.get_queryset().count()

        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        search_filter = self.request.GET.get('search', None)
        status_filter = self.request.GET.get('status', None)

        if status_filter:
            if status_filter in dict(ContactMessage.STATUS_CHOICES).keys():
                queryset = queryset.filter(status=status_filter)

        if search_filter:
            queryset = queryset.filter(Q(code__icontains=search_filter))


        return queryset


class MessageDetailView(LoginRequiredMixin, AdminAccessMixin, generic.DetailView):
    model = ContactMessage
    template_name = 'dashboard/messages/message_detail.html'
    context_object_name = 'message'
    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context["object_name_fa"] = 'پیام'
        context["object_name_fa_plural"] = 'پیام ها'

        return context
    def get_object(self):
        obj = super().get_object()
        # Mark as seen if not already seen
        if obj.status == 'not_seen':
            obj.status = 'seen'
            obj.seen_at = timezone.now()
            obj.save()
        return obj


# --------------------------------- Orders View ---------------------------------
class OrderView(LoginRequiredMixin, AdminAccessMixin, generic.ListView):
    model = SiteInfo
    template_name = 'dashboard/site/site.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_shared_context(self, context):
        context["object_name_fa"] = 'سفارش'
        context["object_name_fa_plural"] = 'سفارشات'

        return context

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context["object_name_fa"] = 'سفارش'
        context["object_name_fa_plural"] = 'سفارشات'
        context['objects_count'] = self.get_queryset().count()
        context['users'] = User.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        user_filter_id = self.request.GET.get('user_filter', None)
        is_paid = self.request.GET.get('is_paid', None)
        status = self.request.GET.get('status', None)
        delivery_option = self.request.GET.get('delivery_option', None)
        search = self.request.GET.get('search', None)

        if user_filter_id and user_filter_id != 'all':
            queryset = queryset.filter(user__id=user_filter_id)

        if is_paid and is_paid != 'None':
            is_paid = is_paid == 'True'
            queryset = queryset.filter(is_paid=is_paid)

        if status and status != 'all':
            queryset = queryset.filter(shipping_status=status)

        if delivery_option and delivery_option != 'all':
            queryset = queryset.filter(delivery_option=delivery_option)

        if search:
            queryset = queryset.filter(Q(code__icontains=search))

        return queryset


class OrderUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = SiteInfo
    fields = ('name', 'logo', 'email', 'phone', 'is_paid',
              'address', 'description', )

    template_name = 'dashboard/site/site.html'
    success_message = 'تغییرات ثبت گردید'

    def get_success_url(self):
        return reverse('dashboard:site')

    def form_valid(self, form):

        return super().form_valid(form)

    def form_invalid(self, form):
        # Add errors to messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{form.fields[field].label}: {error}")

        return self.form_invalid_redirect()

    def form_invalid_redirect(self):
        return redirect(reverse('dashboard:site'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name_fa'] = 'سفارش'
        context['object_name_fa_plural'] = 'سفارشات'
        context['users'] = User.objects.all()

        return context
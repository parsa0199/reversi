from django.db.models import Q,F
from django.views import generic
from django.shortcuts import render
from datetime import datetime, timedelta
from .forms import ContactForm
from django.contrib import messages
from .models import ContactMessage  
# import pandas as pd
import os, csv, io
from django.http import *
import random



def handler404(request, exception, template_name="404.html"):
    return render(request, template_name)


class HomeView(generic.TemplateView):
    template_name = 'main/home.html'




class AboutView(generic.TemplateView):
    template_name = 'main/about.html'


class DiseView(generic.TemplateView):
    template_name = 'main/dise.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if 'roll' is present in the GET parameters to trigger a dice roll
        if 'roll' in self.request.GET:
            # Simulate rolling a 6-sided dice
            context['roll_value'] = random.randint(1, 6)
            if context['roll_value']  == 6 :
                context['result'] = 'شما برنده شدید'
            else:
                context['result'] = 'هفته بعد شاید برنده بشی . این هفته که نشد. '

        else:
            context['roll_value'] = None

        return context

class EduView(generic.TemplateView):
    template_name = 'main/edu.html'

class PrivicyView(generic.TemplateView):
    template_name = 'main/privacy.html'
    
class Privicy2View(generic.TemplateView):
    template_name = 'main/privacy2.html'


class ContactView(generic.FormView):
    template_name = 'main/contact.html'
    form_class = ContactForm
    success_url = '/success/'  # URL صفحه موفقیت

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']

        try:
            # ذخیره اطلاعات در مدل ContactMessage
            contact_message = ContactMessage(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            contact_message.save()

            # نمایش پیغام موفقیت
            messages.success(self.request, 'پیغام شما با موفقیت ارسال شد.')

        except Exception as e:
            # نمایش پیغام خطا
            messages.error(self.request, 'خطایی در ارسال پیغام رخ داد. لطفا دوباره تلاش کنید.')
            print(e)  # چاپ خطا برای بررسی

        # بازگشت به صفحه فعلی
        return self.render_to_response(self.get_context_data(form=form))




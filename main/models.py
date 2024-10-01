from django.db import models
from jalali_date import datetime2jalali, date2jalali
from django.core.validators import MaxLengthValidator
from accounts.validators import phone_number_validator
from .utils import upload_logo_path


class General(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        abstract = True

    def get_created_at(self):
        return datetime2jalali(self.created_at).strftime('%H:%M - %Y/%m/%d')
    get_created_at.short_description = 'تاریخ ایجاد'

    def get_updated_at(self):
        return datetime2jalali(self.updated_at).strftime('%H:%M - %Y/%m/%d')
    get_updated_at.short_description = 'آخرین بروزرسانی'


class SEO(models.Model):
    meta_title = models.TextField(verbose_name="meta title (SEO)", validators=[MaxLengthValidator(160)], \
                                  null=True, help_text="حداکثر 160 کاراکتر")
    meta_description = models.TextField(verbose_name="meta description (SEO)", \
                                        validators=[MaxLengthValidator(160)], null=True, help_text="حداکثر 160 کاراکتر")


# ----------------SMS log---------------------
class SmsLog(General):
    SUBJECT_CHOICES = [
        ('phone_verify', 'تایید موبایل'),
        ('email_verify', 'تایید ایمیل'),
        ('birth_date', 'تبریک تولد'),
        ('new_order_customer', 'سفارش جدید (به مشتری)'),
        ('new_order_admin', 'سفارش جدید (به ادمین)'),
        ('other', 'سایر'),
    ]

    phone = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='کاربر')
    subject = models.CharField(max_length=30, choices=SUBJECT_CHOICES, default='other', verbose_name='موضوع')
    is_sent = models.BooleanField(default=True, verbose_name='وضعیت ارسال')
    status_code = models.PositiveSmallIntegerField(null=True, verbose_name='کد وضعیت')
    description = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'تاریخچه sms'
        verbose_name_plural = 'تاریخچه sms ها'


    # ---------------------contact form model------------------------------------------------


class ContactMessage(models.Model):
    STATUS_CHOICES = (
        ('not_seen', 'جدید'),
        ('seen', 'خوانده شده'),
    )

    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    subject = models.CharField(max_length=200, verbose_name='موضوع')
    message = models.TextField(verbose_name='پیام')
    created_at = models.DateTimeField(auto_now_add=True , verbose_name='تاریخ ایجاد')
    phone = models.CharField("تلفن همراه", null=True, max_length=11, \
                             validators=[phone_number_validator], blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='not_seen',verbose_name='وضعیت')
    seen_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ مشاهده')  # Add this line

    class Meta:
        verbose_name = 'پیام ارتباط با ما'
        verbose_name_plural = 'پیام های ارتباط با ما'
        ordering = ('-created_at',)

    def get_created_at(self):
        return datetime2jalali(self.created_at).strftime('%H:%M - %Y/%m/%d')
    get_created_at.short_description = 'تاریخ ایجاد'
    def get_seen_at(self):
        return datetime2jalali(self.seen_at).strftime('%H:%M - %Y/%m/%d')
    get_created_at.short_description = 'تاریخ مشاهده'

    def __str__(self):
        return self.name
# -------------------------site settings ---------------------------------------------


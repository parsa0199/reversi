from django.db import models
from jalali_date import datetime2jalali
from .utils import upload_logo_path

# -------------------------site settings ---------------------------------------------

class SiteInfo(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام سایت")
    logo = models.ImageField(upload_to=upload_logo_path, blank=True, null=True, verbose_name="لوگو")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    # Contact information
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره تلفن")
    email = models.EmailField(max_length=254, blank=True, null=True, verbose_name="ایمیل")
    address = models.TextField(blank=True, null=True, verbose_name="آدرس")

    # SEO information
    meta_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="عنوان متا")
    meta_description = models.TextField(blank=True, null=True, verbose_name="توضیحات متا")
    meta_keywords = models.CharField(max_length=500, blank=True, null=True, verbose_name="کلمات کلیدی متا")

    # Social media links
    facebook = models.URLField(blank=True, null=True, verbose_name="لینک فیس‌بوک")
    twitter = models.URLField(blank=True, null=True, verbose_name="لینک توییتر")
    instagram = models.URLField(blank=True, null=True, verbose_name="لینک اینستاگرام")
    linkedin = models.URLField(blank=True, null=True, verbose_name="لینک لینکدین")
    youtube = models.URLField(blank=True, null=True, verbose_name="لینک یوتیوب")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین بروزرسانی')

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_created_at(self):
        return datetime2jalali(self.created_at).strftime('%H:%M - %Y/%m/%d')
    get_created_at.short_description = 'تاریخ ایجاد'

    def get_updated_at(self):
        return datetime2jalali(self.updated_at).strftime('%H:%M - %Y/%m/%d')
    get_updated_at.short_description = 'آخرین بروزرسانی'

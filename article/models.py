from django.db import models
from jalali_date import datetime2jalali, date2jalali
from django.core.validators import MaxLengthValidator
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from .utils import upload_image_path, upload_video_path, upload_thumbnail_path
import math
from accounts.models import User  


# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(publish=True)


class ArticleGeneral(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, \
                               verbose_name="نویسنده" ,blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        abstract = True

    def get_created_at(self):
        return datetime2jalali(self.created_at).strftime('%H:%M - %Y/%m/%d')

    get_created_at.short_description = 'تاریخ و زمان ایجاد'

    def get_created_at__date(self):
        return datetime2jalali(self.created_at).strftime('%Y/%m/%d')

    get_created_at__date.short_description = 'تاریخ ایجاد'

    def get_updated_at(self):
        return datetime2jalali(self.updated_at).strftime('%H:%M - %Y/%m/%d')

    get_updated_at.short_description = 'آخرین بروزرسانی'


class SEO(models.Model):
    meta_title = models.TextField(verbose_name="meta title (SEO)", validators=[MaxLengthValidator(60)], \
                                  null=True, help_text="حداکثر 60 کاراکتر")
    meta_description = models.TextField(verbose_name="meta description (SEO)", \
                                        validators=[MaxLengthValidator(160)], null=True, help_text="حداکثر 160 کاراکتر")

    class Meta:
        abstract = True


class Category(ArticleGeneral):
    title = models.CharField(null=True, max_length=128, verbose_name='عنوان')
    views = models.PositiveIntegerField(default=0, verbose_name='بازدیدها')
    slug = models.SlugField(max_length=128, blank=True, null=True, unique=True, \
                            allow_unicode=True, verbose_name='پیوند یکتا', help_text='این فیلد را خالی بگذارید.')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = ' دسته بندی‌ها'
        ordering = ('-created_at',)

    # get category names for category slugs
    def save(self, *args, **kwargs):
        if not self.slug:
            value = self.title
            self.slug = slugify(value, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        if self.title:
            return self.title
        return 'دسته بندی ناشناخته'

    def increment_views(self):
        self.views += 1
        self.save()

    @property
    def get_views(self):
        return self.views + 100


class Article(ArticleGeneral, SEO):
    created_at = models.DateTimeField(verbose_name='تاریخ ایجاد')
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, verbose_name="دسته بندی")
    title = models.CharField(max_length=225, null=True, verbose_name="عنوان مقاله")
    body = RichTextUploadingField(null=True, verbose_name="محتوای مقاله")

    thumbnail = models.ImageField(null=True, upload_to=upload_thumbnail_path, \
                                  verbose_name="تصویر شاخص",
                                  help_text="ابعاد عکس مربعی و حجم آن کمتر از 1 مگابایت باشد.")

    publish = models.BooleanField(default=True, verbose_name="در سایت منتشر شود", \
                                  help_text="غیرفعال بودن این فیلد به معنی پیش نویس بودن مقاله و عدم انتشار آن در سایت می‌باشد.")
    views = models.PositiveIntegerField(default=0, verbose_name="بازدیدها")
    slug = models.SlugField(max_length=225, null=True, blank=True, unique=True, allow_unicode=True,
                            verbose_name="پیوند یکتا")
    reed_time = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="مدت زمان خواندن متن")
    tags = models.ManyToManyField('ArticleTag', related_name='ArticleTag', blank=True, verbose_name="هشتگ‌ها")

    # Model managers
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = '    مقالات'
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.slug:
            # set article slug from title
            article_title = self.title
            self.slug = slugify(article_title, allow_unicode=True)

        # Estimate article reed time
        body = self.body
        words_count = len(body.split())
        self.reed_time = math.ceil(words_count / 100)
        super(Article, self).save(*args, **kwargs)

    def increment_views(self):
        self.views += 1
        self.save()

    def __str__(self):
        return str(self.title)

    def get_views(self):
        return self.views + 100

    def get_absolute_url(self):
        return reverse("article:article-details", kwargs={"slug": self.slug})


# -------------------------------Article Comments-------------------------------
class ArticleComment(models.Model):
    body = models.TextField(max_length=300)
    # replyTo = models.ForeignKey('self', related_name='replays', blank=True, null=True, on_delete=models.PROTECT)
    # parent_id = models.PositiveSmallIntegerField(null=True, blank=True,)
    # parents_id = models.TextField(null=True, blank=True)
    # is_parent = models.BooleanField(default=False)
    created_at = models.DateTimeField(verbose_name='Created Date', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated Date',
                                      auto_now=True)  # تغییر از updated_at_at به updated_at
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(Article, on_delete=models.PROTECT, related_name='comments', verbose_name='مقاله مربوطه')
    active = models.BooleanField(default=False)
    email = models.EmailField()

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        if self.created_by:
            return self.body + " ---------- " + self.created_by.get_username()
        return "unknown user comment"

    # def is_reply(self):
    #     return self.replyTo is not None


# tags in articles
class ArticleTag(SEO, models.Model):
    title = models.CharField(null=True, max_length=225, verbose_name='عنوان')
    description = RichTextField(blank=True, null=True, verbose_name='توضیحات')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, \
                                 blank=True, null=True, related_name="tags", verbose_name='دسته بندی')
    slug = models.SlugField(max_length=225, blank=True, null=True, \
                            unique=True, allow_unicode=True, verbose_name='پیوند یکتا')
    views = models.PositiveIntegerField(default=0, verbose_name='بازدیدها')
    created_at = models.DateTimeField(verbose_name='Created Date', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name='Updated Date', auto_now=True, null=True)

    class Meta:
        verbose_name = 'هشتگ'
        verbose_name_plural = 'هشتگ‌های مقالات'
        ordering = ('-views',)

    # get tag title for tag slugs
    def save(self, *args, **kwargs):
        if not self.slug:
            value = self.title
            self.slug = slugify(value, allow_unicode=True)
        super(ArticleTag, self).save(*args, **kwargs)

    def increment_views(self):
        self.views += 1
        if self.category:
            self.category.increment_views()
        self.save()

    def __str__(self):
        return self.title

    @property
    def get_views(self):
        return self.views + 100

    def get_absolute_url(self):
        return reverse("article:article-tag", kwargs={"tagname": self.slug})


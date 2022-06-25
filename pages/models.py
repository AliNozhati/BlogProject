from django.utils.html import format_html
from account.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from extensions.utils import jalali_converter

# from myproject.myproject.settings import STATIC_URL

# Create your models here.

class ArticleManager(models.Manager): # مدیریت مقاله ها
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager): # مدیریت دسته بندی ها
    def active(self):
        return self.filter(status=True)


class Category(models.Model): # دسته بندی 
    parent = models.ForeignKey('self', related_name='children', default=None, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=("زیردسته"))
    title = models.CharField(max_length=100, verbose_name=("عنوان"))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=("آدرس"))
    status = models.BooleanField(default=True, verbose_name=("وضعیت"))
    position = models.IntegerField(verbose_name=("پوزیشن"))

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
        # return reverse("pages:categoryList", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ['parent__id', 'position']

    objects = CategoryManager()
    

class Article(models.Model): # مقاله
    STATUS_CHOICES = (
        ('d', "پیش نویس"),       # draft
        ('p', "منتشر شده"),      # publish
        ('i', "درحال بررسی"),    # investigation
        ('b', "برگشت داده شده"), # back
    )
    category = models.ManyToManyField(Category, verbose_name=("دسته بندی"), related_name="Articles")
    title = models.CharField(max_length=255, verbose_name=("عنوان"))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=("آدرس"))
    description = models.TextField(verbose_name=("خلاصه"))
    thumbnail = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name=("عکس"))
    publish = models.DateTimeField(default=timezone.now, verbose_name=("زمان انتشار"))
    created = models.DateTimeField(auto_now_add=True) # تاریخ ایجاد
    updated = models.DateTimeField(auto_now=True) # تاریخ اپدیت کردن
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name=("وضعیت"))
    is_special = models.BooleanField(default=False, verbose_name=("ویژه"))

    # on_delete=models.SET_NULL => بعد از حذف شدن نویسنده نال شود
    # on_delete=models.CASCADE => بعد از حذف شدن نویسنده حذف شود
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="Articles", verbose_name=("نویسنده"))

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        
    def category_publeshed(self): # برگرداندن دسته بندی 
        return self.category.filter(status=True) # دسته بندی هایی که انتخاب(صحیح) شده اند

    def __str__(self):
        return self.title

    def jpublish(self): # تدیل کردن تاریخ به شمسی
        return jalali_converter(self.publish)
    jpublish.short_description = "زمان انتشار"

    def get_absolute_url(self): # فرم ها برای ارسال و ریورس کردن به این متد نیاز دارند
        return reverse("account:home")

    def thumbnail_tag(self): # متد برای نمایش عکس در پنل ادمین
        return format_html(f'<img width=100 src ="{self.thumbnail.url}" alt="{self.title}" width=20 height=100 >')

    def categoryToStr(self):
        return ", ".join([category.title for category in self.category_publeshed()])
    categoryToStr.short_description = "دسته بندی"

    objects = ArticleManager()
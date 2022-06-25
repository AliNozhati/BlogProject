from django.contrib import admin
from . models import Article, Category

# Register your models here.

admin.site.site_header = 'وبلاگ'
# admin.site.disable_action("delete_selected")

#  انتخاب و پابلیش کردن
def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
    rows_updated = queryset.update(status='p') # تعداد سطر های انتخاب شده

    if rows_updated == 1:
        message_bit = "منتشر شد"
    else:
        message_bit = "منتشر شدند"

    modeladmin.message_user(request, f'{rows_updated} مقاله {message_bit}.')
make_published.short_description = "انتشار کردن مقالات انتخاب شده"


#  انتخاب و درفت کردن
def make_draft(modeladmin, request, queryset):
    queryset.update(status='d')
    rows_updated = queryset.update(status='d') # تعداد سطر های انتخاب شده

    if rows_updated == 1:
        message_bit = "پیش نویس شد"
    else:
        message_bit = "پیش نویس شدند"

    modeladmin.message_user(request, f'{rows_updated} مقاله {message_bit}.')
make_draft.short_description = "پیش نویس کردن مقالات انتخاب شده"


# کلاس مربوط به دسته بندی ها در پنل ادمین
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position','title', 'parent','slug','status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Category, CategoryAdmin)


# کلاس مربوط به مقاله ها در پنل ادمین
class ArticleAdmin(admin.ModelAdmin):
    # نمایش لیست ها و استفاده از فیلد و یا متد
    list_display = ('title', 'thumbnail_tag', 'author', 'slug', 'jpublish', 'is_special', 'status', 'categoryToStr')
    list_filter = ('publish', 'status', 'author')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug':('title',)}
    ordering = ('status', '-publish')
    actions = [make_published, make_draft]

admin.site.register(Article, ArticleAdmin)
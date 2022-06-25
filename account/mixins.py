from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from pages.models import Article


class FieldMixin():
    def dispatch(self, request, *args, **kwargs):
        self.fields = ['category', 'title', 'slug', 'description', 'thumbnail', 'publish','is_special', 'status']

        # فیلد نویسنده فقط برای ادمین قابل مشاهده هست
        if request.user.is_superuser:
            self.fields.append('author')
        elif not request.user.is_author :
            raise Http404("You can't see this page.")
    
        return super().dispatch(request, *args, **kwargs)
    

# چک کردن فرم
class FormValidMixin():
    def form_valid(self, form):
        # اگر ادمین بود بدون چک سیو میکنیم
        if self.request.user.is_superuser:
            form.save()
        # نویسنده رو خودش میزاریم و اگر دستی هرچیزی بجز ارسال به ادمین زد، خودمون پیش نویس میزاریمش
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if not self.obj.status == 'i':
                self.obj.status = 'd'
        return super().form_valid(form) 
    

# مشاهده صفحه فقط برای نویسنده مقاله ی منتشر شده و یا پیش نویس
class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if ((article.author == request.user and article.status in ['d', 'b']) or\
        request.user.is_superuser):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("You can't see this page.")


# چک کردن ورود کاربر و ریدایرکت کردن با توجه به عنوان کاربر
class AuthorsAcceccMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("account:profile")
        else:
            return redirect("login")


# دسترسی شخصی ادمین
class SuperUserAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("You can't see this page.")
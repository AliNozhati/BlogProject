from django.core.paginator import Paginator
from account.models import User
from django.shortcuts import render, get_object_or_404
from . models import Article, Category
from django.views.generic import TemplateView, ListView, DetailView
from account.mixins import AuthorAccessMixin

# Create your views here.

class templateHomeView(TemplateView): # صفحه اصلی سایت
    template_name = 'pages/home.html'
    

class templateAboutView(TemplateView):
    template_name = 'pages/about.html'


class categoryView(ListView): # نمایش دسته بندی ها
    model = Category
    paginate_by = 4
    template_name = 'pages/category.html'

    def get_queryset(self):
        category = Category.objects.all()
        return category


class userView(ListView): # نمایش مقالات کاربر
    paginate_by = 6
    template_name = 'pages/user.html'

    # گرفتن کاربر با یوزر نیم مشخص و ریترن مقالاتش
    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        article = author.Articles.published()
        return article

    # برگرداندن خود کاربر
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context


class articleListView(ListView): # لیست مفالات
    paginate_by = 7
    template_name = 'pages/listArticle.html'

    def get_queryset(self):
        global article
        article = Article.objects.published()
        return article


class detailArticle(DetailView): # توضیحات مقاله
    model = Article
    template_name = 'pages/detailArticle.html'

# def detailArticle(request, slug):
#     context = {
#         "article": Article.objects.get(slug=slug)
#         # "article": get_object_or_404(Article, slug=slug)
#     }
#     return render(request, "pages/detailArticle.html", context)


class previewArticle(AuthorAccessMixin, DetailView): # نمایش مقاله(منتشر نشده)
    template_name = 'pages/detailArticle.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


class CategoryListView(ListView): # نمایش مقالات یک دسته بندی
    paginate_by = 3
    template_name = 'pages/CategoryListView.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.Articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context
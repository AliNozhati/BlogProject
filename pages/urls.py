from django.urls import path
from . views import (
    detailArticle,
    templateHomeView,
    articleListView,
    templateAboutView,
    categoryView,
    CategoryListView,
    userView,
    previewArticle,
)

app_name = "pages"
urlpatterns = [
    
    path('', templateHomeView.as_view(), name = "homePosts"), # صفحه اصلی سایت
    path('about/', templateAboutView.as_view(), name = "about"), 

    path('category/', categoryView.as_view(), name = "category"), # نمایش دسته بندی ها
    path('category/page/<int:page>', categoryView.as_view(), name = "category"), # نمایش دسته بندی ها

    path('category/<slug:slug>', CategoryListView.as_view(), name = "categoryList"), # نمایش مقالات یک دسته بندی
    path('category/<slug:slug>/page/<int:page>', CategoryListView.as_view(), name = "categoryList"), # نمایش مقالات یک دسته بندی

    path('user/<slug:username>/', userView.as_view(), name = "user"), # مقالات یک کاربر
    path('user/<slug:username>/page/<int:page>/', userView.as_view(), name = "user"), # مقالات یک کاربر
    
    path('articles/', articleListView.as_view(), name = "listArticles"), # نمایش مقالات
    path('articles/page/<int:page>', articleListView.as_view(), name = "listArticles"), # نمایش مقالات

    path('articles/<slug:slug>/', detailArticle.as_view(), name = "detailArticle"), # توضیحات هر مقاله
    path('preview/<int:pk>/', previewArticle.as_view(), name = "previewArticle"), # نمایش مقاله(منتشر نشده)
]
from django.urls import path
from .views import ArticleListView, ArticleCreate, HomeView, ArticleUpdate, ArticleDelete, Profile

app_name = "account"
urlpatterns = [

    path('', HomeView.as_view(), name='home'), # صفحه شخصی

    path('articles/', ArticleListView.as_view(), name='listArticle'), # نمایش لیست مقالات

    path('article/create/', ArticleCreate.as_view(), name='articleCreate'), # ایجاد مقاله
    path('article/update/<int:pk>/', ArticleUpdate.as_view(), name='articleUpdate'), # ویرایش مقاله
    path('article/delete/<int:pk>/', ArticleDelete.as_view(), name='articleDelete'), # حذف مقاله
    
    path('profile/', Profile.as_view(), name='profile'), # مشخصات حساب

]
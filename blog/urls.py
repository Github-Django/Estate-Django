from django.contrib import admin
from django.urls import path, re_path
from .views import *

app_name = 'blog'
urlpatterns = [
    path('', ArticleList, name='home'),
    path('page/<int:page>', ArticleList, name='home'),
    re_path(r'listing/(?:page-(?P<page_number>\d+)/)?$', ListProperty, name='listing'),
    re_path(r'special/(?:page-(?P<page_number>\d+)/)?$', SpecialListing, name='special'),
    re_path(r'grid/(?:page-(?P<page_number>\d+)/)?$', GridProperty, name='grid'),
    re_path(r'category/(?P<slug>[-\w]+)/', CategoryList.as_view(), name="category"),
    path('category/<slug:slug>/page/<int:page>', CategoryList.as_view(), name="category"),
    re_path(r'detail/(?P<slug>[-\w]+)/', ArticleDetail.as_view(), name="detail"),
    path('detail/<slug:slug>-<int:pk>/', ArticleDetail.as_view(), name="detail"),
    path('author/<slug:phone>/', AuthorList.as_view(), name="author"),
    path('author/<slug:phone>/page/<int:page>', AuthorList.as_view(), name="author"),
    path('preview/<int:pk>', ArticlePreview.as_view(), name="preview"),

]
# 👇👇👇👇halat deploy👇👇👇👇

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 👆👆👆👆 halat deploy👆👆👆👆

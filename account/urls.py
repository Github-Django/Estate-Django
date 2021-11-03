from django.urls import path
from .views import ArticleList, ArticleDelete, upload

app_name = "account"

urlpatterns = [
    path('', ArticleList.as_view(), name='home'),
    path('upload/', upload, name="upload"),
    path('delete/<int:pk>', ArticleDelete.as_view(), name='article-delete'),

]

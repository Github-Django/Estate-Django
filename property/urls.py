"""property URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from account.views import user_logout, verify, register_view
from blog.views import notfound

urlpatterns = [
    path('adminnjr/', admin.site.urls),
    path('', include('blog.urls')),
    path('account/', include('account.urls')),
    path('', include('django.contrib.auth.urls')),
    path('logout/', user_logout, name='logout'),
    path('register', register_view, name='register_view'),
    path('verify/', verify, name='verify'),

]
handler404 = 'blog.views.notfound'

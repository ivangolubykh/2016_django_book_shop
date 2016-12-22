"""django_02 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
# from django.contrib import admin
from mainapp.views import *
from authorization.views import *
from django.views.generic.base import RedirectView # для редиректа с главной страницы в папку
from django.conf.urls import url, include



urlpatterns = [
#    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url='django/profile_ig/test_magazine-01/')), # редирект с главной страницы в папку
    url(r'^django/profile_ig/test_magazine-01/', include([
        url(r'^$', main, name='main'),
        url(r'^login/$', login, name='login'),
        url(r'^logout/$', logout, name='logout'),
    ])),


]

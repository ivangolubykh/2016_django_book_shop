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
from mainapp.views import Main
from authorization.views import Login, Logout
from administrations.views import Admin_Main, Admin_View_User_List
from django.views.generic.base import RedirectView # для редиректа с главной страницы в папку
from django.conf.urls import url, include



urlpatterns = [
#    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url='django/profile_ig/test_magazine-01/')), # редирект с главной страницы в папку
    url(r'^django/profile_ig/test_magazine-01/', include([
        url(r'^$', Main, name='main'),
        url(r'^login/$', Login, name='login'),
        url(r'^logout/$', Logout, name='logout'),
    ])),
    url(r'^django/profile_ig/test_magazine-01/admin/', include([
        url(r'^$', Admin_Main, name='admin_main'),
        url(r'^view_user_list/$', Admin_View_User_List, name='view_user_list'),
    ])),

]

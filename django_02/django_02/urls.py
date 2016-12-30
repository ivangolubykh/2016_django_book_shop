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
from mainapp.views import Main, Register_User, List_Books
from authorization.views import Login, Logout
from administrations.views import Admin_Main, Admin_Change_Data, Admin_Books_Authors
from django.views.generic.base import RedirectView # для редиректа с главной страницы в папку
from django.conf.urls import url, include


starturl = r'^django/profile_ig/test_magazine-01/'

urlpatterns = [
#    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url='django/profile_ig/test_magazine-01/')), # редирект с главной страницы в папку
    url(starturl, include([
        url(r'^$', Main, name='main'),
        url(r'^login/$', Login, name='login'),
        url(r'^logout/$', Logout, name='logout'),
        url(r'^registration/$', Register_User, name='register_user'),
    ])),
    url(starturl + 'admin/', include([
        url(r'^$', Admin_Main, name='admin_main'),
        url(r'^view_user_list/$', Admin_Change_Data, name='admin_change_data'),
        url(r'^books/$', Admin_Books_Authors, name='admin_book_author'),
    ])),
]

urlpatterns += [
    url(starturl, include([
        url(r'^book/([\d+])/$', List_Books, name='book'),
    ])),
]

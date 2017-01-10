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
from .views import Admin_Books_Authors, Admin_Books_Categories, Admin_Books

from mainapp.views import Main, Register_User, List_Books

urlpatterns = [
    url(r'^books_authors/$', Admin_Books_Authors, name='admin_book_author'),
    url(r'^books_categories/$', Admin_Books_Categories, name='admin_book_categor'),
    url(r'^books/$', Admin_Books, name='admin_book'),
]

urlpatterns += [
    url(r'^book/([\d+])/$', List_Books, name='book'),
]

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
from .views import MainListView, Register_User, BookDetailView,\
    SearchBookListView, CategoryListView, CategoryDetailView, Transport


urlpatterns = [
    url(r'^$', MainListView.as_view(), name='main'),
    url(r'^registration/$', Register_User, name='register_user'),
    url(r'^book/(?P<pk>[\d]+)/$', BookDetailView.as_view(), name='book'),
    url(r'^search/$', SearchBookListView.as_view(), name='search'),
    url(r'^category/$', CategoryListView.as_view(), name='category'),
    url(r'^category/(?P<pk>[\d]+)/$', CategoryDetailView.as_view(),
        name='category_detail'),
    url(r'^transport/$', Transport, name='transport'),
]

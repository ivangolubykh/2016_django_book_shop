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
#from admin_book.views import Admin_Main, Admin_Change_Data, Admin_Books_Authors, Admin_Books_Categories, Admin_Books
from django.views.generic.base import RedirectView # для редиректа с главной страницы в папку
from django.conf.urls import url, include

# для раздачи медиа ТОЛЬКО на ТЕСТОВОМ сервере
from django.conf import settings
from django.conf.urls.static import static

starturl = r'^django/profile_ig/test_magazine-01/'

urlpatterns = [
#    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url='django/profile_ig/test_magazine-01/')), # редирект с главной страницы в папку
    url(starturl, include([
        url(r'^$', Main, name='main'),
        url(r'^registration/$', Register_User, name='register_user'),
    ])),
    # url(starturl + 'admin/', include([
    #     url(r'^$', Admin_Main, name='admin_main'),
    #     url(r'^view_user_list/$', Admin_Change_Data, name='admin_change_data'),
    #     url(r'^books_authors/$', Admin_Books_Authors, name='admin_book_author'),
    #     url(r'^books_categories/$', Admin_Books_Categories, name='admin_book_categor'),
    #     url(r'^books/$', Admin_Books, name='admin_book'),
    # ])),
]

urlpatterns += [
    url(starturl + 'authorization/', include('authorization.urls')),
]
urlpatterns += [
    url(starturl + 'admin_users/', include('admin_users.urls')),
]
urlpatterns += [
    url(starturl + 'admin_book/', include('admin_book.urls')),
]


urlpatterns += [
    url(starturl, include([
        url(r'^book/([\d+])/$', List_Books, name='book'),
    ])),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # для раздачи медиа ТОЛЬКО на ТЕСТОВОМ сервере

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

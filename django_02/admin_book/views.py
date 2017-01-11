from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .forms import Edit_Book_Author, Edit_Book_Categories, Edit_Books
from .models import Books_Author, Books_Categories, Books

#from django.http import Http404, JsonResponse
#from django.template import loader


########################
# Это приложение зависит от приложения "authorization" и от путей к другим страницам
# сайта в верхнем меню.
# Чтобы отменить эту зависимость, надо отредктировать шаблон admin_users_base.html
# 1) убрать строку 26 "{% include 'authorization/box_login.html' %}"
# 2) отредактировать пути в строчках 18-22, например такие: "<a href="{% url 'main' %}">Главная страница сайта</a>"
# на существующие в проекте.
########################


def Veryfy_Admin_Autorizations(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return True
        else:
            return HttpResponse('Ошибка: У вас нет права администрировать.', content_type='text/html; charset=utf-8')
    else:
        return HttpResponse('Ошибка: Вы не авторизованы', content_type='text/html; charset=utf-8', charset='utf-8')



def List_Edit_item(request, model, form_edit, sortBy, external_indexes, template_page, template_list, template_editing,
                   template_info):
    if Veryfy_Admin_Autorizations(request):
        list = model.objects.prefetch_related(*external_indexes).order_by(sortBy)
        if request.method == "POST" and request.is_ajax:
            try:
                change_data = request.POST['change_data']
            except:
                return HttpResponse('Ошибка: 001', content_type='text/html; charset=utf-8')
                # 001 - Ошибка запроса. Нет change_data

            if change_data == 'item_list':
                add_form = form_edit(request.POST, request.FILES)
                if add_form.is_valid():
                    add_form.save()
                    return render(request, template_list, {'form_item_add': form_edit(), 'item_list': list})
                return render(request, template_list, {'form_item_add': add_form, 'item_list': list})

            elif change_data == 'item_start_edit':
                try:
                    edit_id = request.POST['item_id']
                except:
                    return HttpResponse('Ошибка: 006', content_type='text/html; charset=utf-8')
                    # 006 - Ошибка запроса. Нет item_id
                items = get_object_or_404(model, id=edit_id)
                return render(request, template_editing, {'form_item_edit': form_edit(instance=items), 'id': edit_id})

            elif change_data == 'item_end_edit':
                try:
                    edit_id = request.POST['item_id']
                except:
                    return HttpResponse('Ошибка: 006', content_type='text/html; charset=utf-8')
                    # 006 - Ошибка запроса. Нет item_id
                item_editing = get_object_or_404(model, id=edit_id)
                form = form_edit(request.POST or None, instance=item_editing)
                if form.is_valid():
                    form.save()
                    item = model.objects.prefetch_related(*external_indexes).get(id=edit_id)
                    return render(request, template_info, {'item': item})
                else:
                    return render(request, template_editing, {'form_item_edit': form, 'id': edit_id})

            elif change_data == 'item_deleted':
                try:
                    del_id = request.POST['item_id']
                except:
                    del_id = ''
                if del_id:
                    user = get_object_or_404(model, id=del_id)
                    if user:
                        user.delete()
                        return HttpResponse('<p>Объект удалён успешно.</p>', content_type='text/html; charset=utf-8', charset='utf-8')
                    else:
                        return HttpResponse('Ошибка: Такого объекта нет в БД.', content_type='text/html; charset=utf-8', charset='utf-8')
                else:
                    return HttpResponse('Ошибка: 004', content_type='text/html; charset=utf-8', charset='utf-8')
                    # 004 - Ошибка: передан некорректный id (или не передан вовсе).

            elif change_data == 'item_stop_edit':
                try:
                    stop_edit_id = request.POST['item_id']
                except:
                    stop_edit_id = ''
                if stop_edit_id:
                    item = model.objects.prefetch_related(*external_indexes).get(id=stop_edit_id)
                    if item:
                        return render(request, template_info, {'item': item})
                    else:
                        return HttpResponse('Ошибка: Такого объекта нет в БД.', content_type='text/html; charset=utf-8', charset='utf-8')
                else:
                    return HttpResponse('Ошибка: 004', content_type='text/html; charset=utf-8', charset='utf-8')
                    # 004 - Ошибка: передан некорректный id (или не передан вовсе).

            else:
                return HttpResponse('Ошибка: 002', content_type='text/html; charset=utf-8')
                # 002 - Ошибка запроса. change_data недопустимая
        else:
            return render(request, template_page, {'form_item_add': form_edit, 'item_list': list})




def Admin_Books_Authors(request):
    # запрос, модель, форма, сортировать по, внешние индексы, шаблон страницы,
        # шаблон блока списка элементов, шаблон длока редактирования элемента,
        # шаблон блока одного элемента списка
    external_indexes = ()
    return List_Edit_item(request, Books_Author, Edit_Book_Author, 'baauthor', external_indexes, 'admin_book/adminn_books_authors.html',
                          'admin_book/admin_box_books_authors_list.html', 'admin_book/admin_box_books_author_editing.html',
                          'admin_book/admin_box_books_author_info.html')


def Admin_Books_Categories(request):
    # запрос, модель, форма, сортировать по, внешние индексы, шаблон страницы,
        # шаблон блока списка элементов, шаблон длока редактирования элемента,
        # шаблон блока одного элемента списка
    external_indexes = ()
    return List_Edit_item(request, Books_Categories, Edit_Book_Categories, 'bcname', external_indexes, 'admin_book/adminn_books_categor.html',
                          'admin_book/admin_box_books_categor_list.html', 'admin_book/admin_box_books_categor_editing.html',
                          'admin_book/admin_box_books_categor_info.html')


def Admin_Books(request):
    # запрос, модель, форма, сортировать по, внешние индексы, шаблон страницы,
        # шаблон блока списка элементов, шаблон длока редактирования элемента,
        # шаблон блока одного элемента списка
    external_indexes = ('bauthor', 'bcategories')
    return List_Edit_item(request, Books, Edit_Books, 'bname', external_indexes, 'admin_book/adminn_books.html',
                          'admin_book/admin_box_books_list.html', 'admin_book/admin_box_books_editing.html',
                          'admin_book/admin_box_books_info.html')




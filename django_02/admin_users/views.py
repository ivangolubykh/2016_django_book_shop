from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from admin_users.forms import Edit_User_Form, Edit_User_Passw
# from django.http import Http404, JsonResponse
# from django.template import loader


########################
# Это приложение зависит от приложения "authorization" и от путей к другим
# страницам сайта в верхнем меню.
# Чтобы отменить эту зависимость, надо отредктировать шаблон
#  admin_users_base.html
# 1) убрать строку 26 "{% include 'authorization/box_login.html' %}"
# 2) отредактировать пути в строчках 18-22, например такие:
# <a href="{% url 'main' %}">Главная страница сайта</a>
# на существующие в проекте.
########################

ITEMS_TO_PAGE = 5  # количество элементов на странице


def is_admin(func_to_decorate):
    '''Декоратор для проверки, является ли посетитель админом.'''
    def decor(*args, **kwargs):
        if args[0].user.is_authenticated:
            if args[0].user.is_staff or args[0].user.is_superuser:
                return func_to_decorate(*args, **kwargs)
            else:
                return HttpResponse(
                    'Ошибка: У вас нет права администрировать.',
                    content_type='text/html; charset=utf-8')
        else:
            return HttpResponse('Ошибка: Вы не авторизованы',
                                content_type='text/html; charset=utf-8',
                                charset='utf-8')
    return decor


# @is_admin
def Admin_Main(request):
    list = User.objects.order_by('username')
    paginator = Paginator(list, ITEMS_TO_PAGE)
    return render(request, 'admin_users/admin_users_base.html',
                  {'list': paginator.page(1)})


@is_admin
def Admin_Change_Data(request):
    if request.method == "POST" and request.is_ajax:
        try:
            change_data = request.POST['change_data']
        except:
            return HttpResponse('Ошибка: 001',
                                content_type='text/html; charset=utf-8')
            # 001 - Ошибка запроса. Нет change_data

        if change_data == 'userlist':
            list = User.objects.order_by('username')
            # количество элементов на странице:
            paginator = Paginator(list, ITEMS_TO_PAGE)
            try:
                page = request.POST['page_num']
            except:
                page = 1
            try:
                list = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                list = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999),
                #  deliver last page of results.
                list = paginator.page(paginator.num_pages)
            return render(request, 'admin_users/admin_userlist.html',
                          {'list': list})
            # Если надо отправить без http-заголовка
            # html = loader.\
            #     render_to_string('admin_users/admin_userlist.html',
            #                      {'list': list}, request=request)
            # data = {'errors': False, 'html': html}
            # return JsonResponse(data)

        elif change_data == 'item_start_edit':
            try:
                item_id = request.POST['item_id']
            except:
                item_id = False
            user = get_object_or_404(User, id=item_id)
            return render(request, 'admin_users/admin_useredit.html',
                          {'form': Edit_User_Form(instance=user),
                           'formpassw': Edit_User_Passw(user),
                           'id': item_id})

        elif change_data == 'item_stop_edit':
            try:
                stop_item_id = request.POST['item_id']
            except:
                stop_item_id = False
            if stop_item_id:
                try:
                    item = User.objects.get(id=stop_item_id)
                except:
                    item = False
                if item:
                    return render(request,
                                  'admin_users/admin_box_user_info.html',
                                  {'item': item})
                else:
                    return HttpResponse('<td colspan="10">Ошибка: Такого'
                                        ' объекта нет в БД.</td>',
                                        content_type='text/html;'
                                                     ' charset=utf-8',
                                        charset='utf-8')
            else:
                return HttpResponse('<td colspan="10">Ошибка: 004</td>',
                                    content_type='text/html;'
                                                 ' charset=utf-8',
                                    charset='utf-8')
                # 004 - Ошибка: передан некорректный id
                # (или не передан вовсе).

        elif change_data == 'item_edit':
            user = get_object_or_404(User, id=request.POST['id'])
            form = Edit_User_Form(request.POST or None, instance=user)
            if form.is_valid():
                form.save()
                return render(request,
                              'admin_users/admin_box_user_info.html',
                              {'item': user})

            else:
                return render(request, 'admin_users/admin_useredit.html',
                              {'form': form, 'id': request.POST['id'],
                               'errors': form.errors,
                               'formpassw': Edit_User_Passw(user)})

        elif change_data == 'item_delete':
            try:
                del_id = request.POST['item_id']
            except:
                del_id = False
            if del_id:
                user = get_object_or_404(User, id=del_id)
                if user:
                    user.delete()
                    return HttpResponse('<td colspan="10">Данные успешно'
                                        ' удалены.</td>',
                                        content_type='text/html;'
                                                     ' charset=utf-8',
                                        charset='utf-8')
                else:
                    return HttpResponse('<td colspan="10">Ошибка: Такого'
                                        ' пользователя итак нет в'
                                        ' БД.</td>',
                                        content_type='text/html;'
                                                     ' charset=utf-8',
                                        charset='utf-8')
            else:
                return HttpResponse('<td colspan="10">Ошибка: 004</td>',
                                    content_type='text/html;'
                                                 ' charset=utf-8',
                                    charset='utf-8')
                # 004 - Ошибка: передан некорректный id
                # (или не передан вовсе).

        elif change_data == 'item_edit_passw':
            user = get_object_or_404(User, id=request.POST['id'])
            form = Edit_User_Form(instance=user)
            # formpassw = User.objects.get(id=request.POST['id'])
            formpassw = get_object_or_404(User, id=request.POST['id'])
            formpassw = Edit_User_Passw(formpassw, request.POST or None)
            if formpassw.is_valid():
                formpassw.save()
                return render(request,
                              'admin_users/admin_box_user_info.html',
                              {'item': user})
            else:
                return render(request, 'admin_users/admin_useredit.html',
                              {'form': form, 'id': request.POST['id'],
                               'errors_passw': formpassw.errors,
                               'formpassw': formpassw})

        else:
            return HttpResponse('Ошибка: 002',
                                content_type='text/html; charset=utf-8')
            # 002 - Ошибка запроса. change_data недопустимая
    else:
        return HttpResponse('Ошибка: 003',
                            content_type='text/html; charset=utf-8')
        # 003 - Ошибка: Не ajax или не POST

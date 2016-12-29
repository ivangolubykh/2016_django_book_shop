from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from administrations.forms import Edit_User_Form, Edit_User_Passw, Edit_Book_Author
from mainapp.models import Books_Author

#from django.http import Http404, JsonResponse
#from django.template import loader


def Admin_Main(request):
    users_data = User.objects.values('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'is_staff', 'date_joined', 'last_login', ).order_by('username')
    return render(request, 'administrations/admin_base.html', {'users_data': users_data})


def Veryfy_Admin_Autorizations(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return True
        else:
            return HttpResponse('Ошибка: У вас нет права администрировать.', content_type='text/html; charset=utf-8')
    else:
        return HttpResponse('Ошибка: Вы не авторизованы', content_type='text/html; charset=utf-8', charset='utf-8')


def Admin_Change_Data(request):
    if Veryfy_Admin_Autorizations(request):
        if request.method == "POST" and request.is_ajax:
            try:
                change_data = request.POST['change_data']
            except:
                return HttpResponse('Ошибка: 001', content_type='text/html; charset=utf-8')
                # 001 - Ошибка запроса. Нет change_data
            if change_data  == 'userlist':
                users_data = User.objects.values('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'is_staff', 'date_joined', 'last_login', ).order_by('username')
                return render(request, 'administrations/admin_userlist.html', {'users_data': users_data})
                # Если надо отправить без http-заголовка
                # html = loader.render_to_string('administrations/admin_userlist.html', {'users_data': users_data}, request=request)
                # data = {'errors': False, 'html': html}
                # return JsonResponse(data)
            elif change_data == 'userinfo':
                try:
                    info_id = request.POST['info_id']
                except:
                    info_id = ''
                user = get_object_or_404(User, id=info_id)
                return render(request, 'administrations/admin_useredit.html', {'form': Edit_User_Form(instance=user), 'formpassw': Edit_User_Passw(user), 'id': info_id})
            elif change_data == 'useredit':
                user = get_object_or_404(User, id=request.POST['id'])
                form = Edit_User_Form(request.POST or None, instance=user)
                if form.is_valid():
                    form.save()
                    return HttpResponse('Данные успешно отредактированы.', content_type='text/html; charset=utf-8', charset='utf-8')
                else:
                    return render(request, 'administrations/admin_useredit.html', {'form': form, 'id': request.POST['id'], 'errors': form.errors, 'formpassw': Edit_User_Passw(user)})
            elif change_data == 'useredit_passw':
                form = get_object_or_404(User, id=request.POST['id'])
                form = Edit_User_Form(instance=form)
                # formpassw = User.objects.get(id=request.POST['id'])
                formpassw = get_object_or_404(User, id=request.POST['id'])
                formpassw = Edit_User_Passw(formpassw, request.POST or None)
                if formpassw.is_valid():
                    formpassw.save()
                    return HttpResponse('Пароль отредактирован.', content_type='text/html; charset=utf-8', charset='utf-8')
                else:
                    return render(request, 'administrations/admin_useredit.html', {'form': form, 'id': request.POST['id'], 'errors_passw': formpassw.errors, 'formpassw': formpassw})

            elif change_data == 'userdelete':
                try:
                    del_id = request.POST['del_id']
                except:
                    del_id = ''
                if del_id:
                    user = get_object_or_404(User, id=del_id)
                    if user:
                        user.delete()
                        return HttpResponse('Данные успешно удалены.', content_type='text/html; charset=utf-8', charset='utf-8')
                    else:
                        return HttpResponse('Ошибка: Такого пользователя итак нет в БД.', content_type='text/html; charset=utf-8', charset='utf-8')
                else:
                    return HttpResponse('Ошибка: 004', content_type='text/html; charset=utf-8', charset='utf-8')
                    # 004 - Ошибка: передан некорректный id (или не передан вовсе).

            else:
                return HttpResponse('Ошибка: 002', content_type='text/html; charset=utf-8')
                # 002 - Ошибка запроса. change_data недопустимая
        else:
            return HttpResponse('Ошибка: 003', content_type='text/html; charset=utf-8')
            # 003 - Ошибка: Не ajax или не POST




def Admin_Books(request):
    if Veryfy_Admin_Autorizations(request):
        authors = Books_Author.objects.order_by('baauthor')
        if request.method == "POST" and request.is_ajax:
            try:
                change_data = request.POST['change_data']
            except:
                return HttpResponse('Ошибка: 001', content_type='text/html; charset=utf-8')
                # 001 - Ошибка запроса. Нет change_data
            if change_data == 'book_author_list':
                add_form = Edit_Book_Author(request.POST)
                if add_form.is_valid():
                    add_form.save()
                    return render(request, 'administrations/admin_box_books_list.html', {'form_author_add': Edit_Book_Author(), 'author_list': authors})
                return render(request, 'administrations/admin_box_books_list.html', {'form_author_add': add_form, 'author_list': authors})
            elif change_data == 'book_author_start_edit':
                try:
                    edit_id = request.POST['author_id']
                except:
                    return HttpResponse('Ошибка: 005', content_type='text/html; charset=utf-8')
                    # 005 - Ошибка запроса. Нет author_id
                author = get_object_or_404(Books_Author, id=edit_id)

                return render(request, 'administrations/admin_box_books_author_editing.html', {'form_author_edit': Edit_Book_Author(instance=author), 'id': edit_id})
            elif change_data == 'book_author_end_edit':
                try:
                    edit_id = request.POST['author_id']
                except:
                    return HttpResponse('Ошибка: 005', content_type='text/html; charset=utf-8')
                    # 005 - Ошибка запроса. Нет author_id
                author_editing = get_object_or_404(Books_Author, id=edit_id)
                form = Edit_Book_Author(request.POST or None, instance=author_editing)
                if form.is_valid():
                    form.save()
                    author = Books_Author.objects.values('id', 'baauthor').get(id=edit_id)
                    return render(request, 'administrations/admin_box_books_author_info.html', {'author': author})
                else:
                    return render(request, 'administrations/admin_box_books_author_editing.html', {'form_author_edit': Edit_Book_Author(instance=author_editing), 'id': edit_id})
            elif change_data == 'book_author_deleted':
                try:
                    del_id = request.POST['author_id']
                except:
                    del_id = ''
                if del_id:
                    user = get_object_or_404(Books_Author, id=del_id)
                    if user:
                        user.delete()
                        return HttpResponse('Автор удалён успешно.', content_type='text/html; charset=utf-8', charset='utf-8')
                    else:
                        return HttpResponse('Ошибка: Такого автора итак нет в БД.', content_type='text/html; charset=utf-8', charset='utf-8')
                else:
                    return HttpResponse('Ошибка: 004', content_type='text/html; charset=utf-8', charset='utf-8')
                    # 004 - Ошибка: передан некорректный id (или не передан вовсе).
            else:
                return HttpResponse('Ошибка: 002', content_type='text/html; charset=utf-8')
                # 002 - Ошибка запроса. change_data недопустимая
        else:
            return render(request, 'administrations/adminn_books.html', {'form_author_add': Edit_Book_Author(), 'author_list': authors})





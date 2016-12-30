from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from administrations.forms import Edit_User_Form, Edit_User_Passw, Edit_Book_Author, Edit_Book_Categories, Edit_Books
from mainapp.models import Books_Author, Books_Categories, Books

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




def Admin_Books_Authors(request):
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
                    return render(request, 'administrations/admin_box_books_authors_list.html', {'form_author_add': Edit_Book_Author(), 'author_list': authors})
                return render(request, 'administrations/admin_box_books_authors_list.html', {'form_author_add': add_form, 'author_list': authors})

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
                    return render(request, 'administrations/admin_box_books_author_editing.html', {'form_author_edit': form, 'id': edit_id})

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

            elif change_data == 'book_author_stop_edit':
                try:
                    stop_ediy_id = request.POST['author_id']
                except:
                    stop_ediy_id = ''
                if stop_ediy_id:
                    author = Books_Author.objects.values('id', 'baauthor').get(id=stop_ediy_id)
                    if author:
                        return render(request, 'administrations/admin_box_books_author_info.html', {'author': author})
                    else:
                        return HttpResponse('Ошибка: Такого автора итак нет в БД.', content_type='text/html; charset=utf-8', charset='utf-8')
                else:
                    return HttpResponse('Ошибка: 004', content_type='text/html; charset=utf-8', charset='utf-8')
                    # 004 - Ошибка: передан некорректный id (или не передан вовсе).

            else:
                return HttpResponse('Ошибка: 002', content_type='text/html; charset=utf-8')
                # 002 - Ошибка запроса. change_data недопустимая
        else:
            return render(request, 'administrations/adminn_books_authors.html', {'form_author_add': Edit_Book_Author(), 'author_list': authors})




def Admin_Books_Categories(request):
    if Veryfy_Admin_Autorizations(request):
        categories = Books_Categories.objects.order_by('bcname')
        if request.method == "POST" and request.is_ajax:
            try:
                change_data = request.POST['change_data']
            except:
                return HttpResponse('Ошибка: 001', content_type='text/html; charset=utf-8')
                # 001 - Ошибка запроса. Нет change_data

            if change_data == 'book_categor_list':
                add_form = Edit_Book_Categories(request.POST)
                if add_form.is_valid():
                    add_form.save()
                    return render(request, 'administrations/admin_box_books_categor_list.html', {'form_categor_add': Edit_Book_Categories(), 'categor_list': categories})
                return render(request, 'administrations/admin_box_books_categor_list.html', {'form_categor_add': add_form, 'categor_list': categories})

            elif change_data == 'book_categor_start_edit':
                try:
                    edit_id = request.POST['categor_id']
                except:
                    return HttpResponse('Ошибка: 006', content_type='text/html; charset=utf-8')
                    # 006 - Ошибка запроса. Нет categor_id
                categor = get_object_or_404(Books_Categories, id=edit_id)

                return render(request, 'administrations/admin_box_books_categor_editing.html', {'form_categor_edit': Edit_Book_Categories(instance=categor), 'id': edit_id})

            elif change_data == 'book_categor_end_edit':
                try:
                    edit_id = request.POST['categor_id']
                except:
                    return HttpResponse('Ошибка: 006', content_type='text/html; charset=utf-8')
                    # 006 - Ошибка запроса. Нет categor_id
                categor_editing = get_object_or_404(Books_Categories, id=edit_id)
                form = Edit_Book_Categories(request.POST or None, instance=categor_editing)
                if form.is_valid():
                    form.save()
                    categor = Books_Categories.objects.values('id', 'bcname', 'bcdescr').get(id=edit_id)
                    return render(request, 'administrations/admin_box_books_categor_info.html', {'categor': categor})
                else:
                    return render(request, 'administrations/admin_box_books_categor_editing.html', {'form_categor_edit': form, 'id': edit_id})

            elif change_data == 'book_categor_deleted':
                try:
                    del_id = request.POST['categor_id']
                except:
                    del_id = ''
                if del_id:
                    user = get_object_or_404(Books_Categories, id=del_id)
                    if user:
                        user.delete()
                        return HttpResponse('Категория удалена успешно.', content_type='text/html; charset=utf-8', charset='utf-8')
                    else:
                        return HttpResponse('Ошибка: Такой категории в БД.', content_type='text/html; charset=utf-8', charset='utf-8')
                else:
                    return HttpResponse('Ошибка: 004', content_type='text/html; charset=utf-8', charset='utf-8')
                    # 004 - Ошибка: передан некорректный id (или не передан вовсе).

            elif change_data == 'book_categor_stop_edit':
                try:
                    stop_edit_id = request.POST['categor_id']
                except:
                    stop_edit_id = ''
                if stop_edit_id:
                    categor = Books_Categories.objects.values('id', 'bcname', 'bcdescr').get(id=stop_edit_id)
                    if categor:
                        return render(request, 'administrations/admin_box_books_categor_info.html', {'categor': categor})
                    else:
                        return HttpResponse('Ошибка: Такой категории нет в БД.', content_type='text/html; charset=utf-8', charset='utf-8')
                else:
                    return HttpResponse('Ошибка: 004', content_type='text/html; charset=utf-8', charset='utf-8')
                    # 004 - Ошибка: передан некорректный id (или не передан вовсе).

            else:
                return HttpResponse('Ошибка: 002', content_type='text/html; charset=utf-8')
                # 002 - Ошибка запроса. change_data недопустимая
        else:
            return render(request, 'administrations/adminn_books_categor.html', {'form_categor_add': Edit_Book_Categories(), 'categor_list': categories})




def Admin_Books(request):
    if Veryfy_Admin_Autorizations(request):
        books = Books.objects.values('id', 'bname', 'bauthor__baauthor', 'bcategories__bcname', 'brating', 'bcdateadd', 'bimagelarge').order_by('bname')
        if request.method == "POST" and request.is_ajax:
            try:
                change_data = request.POST['change_data']
            except:
                return HttpResponse('Ошибка: 001', content_type='text/html; charset=utf-8')
                # 001 - Ошибка запроса. Нет change_data

            if change_data == 'book_list':
                add_form = Edit_Books(request.POST, request.FILES)
                if add_form.is_valid():
                    add_form.save()
                    return render(request, 'administrations/admin_box_books_list.html', {'form_book_add': Edit_Books(), 'books_list': books})
                return render(request, 'administrations/admin_box_books_list.html', {'form_book_add': add_form, 'books_list': books})

            elif change_data == 'book_start_edit':
                try:
                    edit_id = request.POST['book_id']
                except:
                    return HttpResponse('Ошибка: 006', content_type='text/html; charset=utf-8')
                    # 006 - Ошибка запроса. Нет book_id
                books = get_object_or_404(Books, id=edit_id)
                return render(request, 'administrations/admin_box_books_editing.html', {'form_book_edit': Edit_Books(instance=books), 'id': edit_id})

            elif change_data == 'book_end_edit':
                try:
                    edit_id = request.POST['book_id']
                except:
                    return HttpResponse('Ошибка: 006', content_type='text/html; charset=utf-8')
                    # 006 - Ошибка запроса. Нет categor_id
                book_editing = get_object_or_404(Books, id=edit_id)
                form = Edit_Books(request.POST or None, instance=book_editing)
                if form.is_valid():
                    form.save()
                    book = Books.objects.values('id', 'bname', 'bauthor__baauthor', 'bcategories__bcname', 'brating', 'bcdateadd', 'bimagelarge').get(id=edit_id)
                    return render(request, 'administrations/admin_box_books_info.html', {'book': book})
                else:
                    return render(request, 'administrations/admin_box_books_editing.html', {'form_book_edit': form, 'id': edit_id})

            elif change_data == 'book_deleted':
                try:
                    del_id = request.POST['book_id']
                except:
                    del_id = ''
                if del_id:
                    user = get_object_or_404(Books, id=del_id)
                    if user:
                        user.delete()
                        return HttpResponse('Книга удалена успешно.', content_type='text/html; charset=utf-8', charset='utf-8')
                    else:
                        return HttpResponse('Ошибка: Такой книги в БД.', content_type='text/html; charset=utf-8', charset='utf-8')
                else:
                    return HttpResponse('Ошибка: 004', content_type='text/html; charset=utf-8', charset='utf-8')
                    # 004 - Ошибка: передан некорректный id (или не передан вовсе).

            elif change_data == 'book_stop_edit':
                try:
                    stop_edit_id = request.POST['book_id']
                except:
                    stop_edit_id = ''
                if stop_edit_id:
                    book = Books.objects.values('id', 'bname', 'bauthor__baauthor', 'bcategories__bcname', 'brating', 'bcdateadd', 'bimagelarge').get(id=stop_edit_id)
                    if book:
                        return render(request, 'administrations/admin_box_books_info.html', {'book': book})
                    else:
                        return HttpResponse('Ошибка: Такой категории нет в БД.', content_type='text/html; charset=utf-8', charset='utf-8')
                else:
                    return HttpResponse('Ошибка: 004', content_type='text/html; charset=utf-8', charset='utf-8')
                    # 004 - Ошибка: передан некорректный id (или не передан вовсе).

            else:
                return HttpResponse('Ошибка: 002', content_type='text/html; charset=utf-8')
                # 002 - Ошибка запроса. change_data недопустимая
        else:
            return render(request, 'administrations/adminn_books.html', {'form_book_add': Edit_Books(), 'books_list': books})




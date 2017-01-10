from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from admin_users.forms import Edit_User_Form, Edit_User_Passw
from mainapp.models import Books_Author, Books_Categories, Books

#from django.http import Http404, JsonResponse
#from django.template import loader


def Admin_Main(request):
    users_data = User.objects.values('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'is_staff', 'date_joined', 'last_login', ).order_by('username')
    return render(request, 'admin_users/admin_base.html', {'users_data': users_data})


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
                return render(request, 'admin_users/admin_userlist.html', {'users_data': users_data})
                # Если надо отправить без http-заголовка
                # html = loader.render_to_string('admin_users/admin_userlist.html', {'users_data': users_data}, request=request)
                # data = {'errors': False, 'html': html}
                # return JsonResponse(data)
            elif change_data == 'userinfo':
                try:
                    info_id = request.POST['info_id']
                except:
                    info_id = ''
                user = get_object_or_404(User, id=info_id)
                return render(request, 'admin_users/admin_useredit.html', {'form': Edit_User_Form(instance=user), 'formpassw': Edit_User_Passw(user), 'id': info_id})
            elif change_data == 'useredit':
                user = get_object_or_404(User, id=request.POST['id'])
                form = Edit_User_Form(request.POST or None, instance=user)
                if form.is_valid():
                    form.save()
                    return HttpResponse('Данные успешно отредактированы.', content_type='text/html; charset=utf-8', charset='utf-8')
                else:
                    return render(request, 'admin_users/admin_useredit.html', {'form': form, 'id': request.POST['id'], 'errors': form.errors, 'formpassw': Edit_User_Passw(user)})
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
                    return render(request, 'admin_users/admin_useredit.html', {'form': form, 'id': request.POST['id'], 'errors_passw': formpassw.errors, 'formpassw': formpassw})

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


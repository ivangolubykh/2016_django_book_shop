from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
from django.http import HttpResponse


def Admin_Main(request):
    users_data = User.objects.values('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'is_staff', 'date_joined', 'last_login', ).order_by('username')
    return render(request, 'administrations/admin_base.html', {'users_data': users_data})


def Admin_Change_Data(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            if request.method == "POST" and request.is_ajax:
                try:
                    change_data = request.POST['change_data']
                except:
                    return HttpResponse('Ошибка: 001', content_type='text/html; charset=utf-8')
                    # 001 - Ошибка запроса. Нет change_data
                users_data = User.objects.values('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'is_staff', 'date_joined', 'last_login', ).order_by('username')
                if change_data  == 'userlist':
                    return render(request, 'administrations/admin_userlist.html', {'users_data': users_data})
                elif change_data  == 'userlist':
                    return render(request, 'administrations/admin_userlist.html', {'users_data': users_data})
                else:
                    return HttpResponse('Ошибка: 002', content_type='text/html; charset=utf-8')
                    # 002 - Ошибка запроса. work_count недопустимый
            else:
                return HttpResponse('Ошибка: 003', content_type='text/html; charset=utf-8')
                # 003 - Ошибка: Не ajax или не POST
        else:
            return HttpResponse('Ошибка: У вас нет права администрировать.', content_type='text/html; charset=utf-8')
    else:
        return HttpResponse('Ошибка: Вы не авторизованы', content_type='text/html; charset=utf-8', charset='utf-8')



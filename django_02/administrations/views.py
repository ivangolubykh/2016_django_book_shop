from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

def Admin_Main(request):
    users_data = User.objects.values('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'is_staff', 'date_joined', 'last_login', ).order_by('username')
    return render(request, 'administrations/admin_base.html', {'users_data': users_data})


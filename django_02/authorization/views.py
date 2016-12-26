from django.contrib import auth

# Create your views here.
from django.shortcuts import render
from general_function.general_function import Return_to_back
from django.http import Http404


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
#        if user is not None:
        if user:
            auth.login(request, user)
            return Return_to_back(request)
        else:
            return render(request, 'index.html', {'erros': 'true'})
    else:
#        raise Http404
        return Return_to_back(request)

def Logout(request):
    auth.logout(request)
    return Return_to_back(request)

from django.contrib import auth
from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404

# Create your views here.

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
#        if user is not None:
        if user:
            auth.login(request, user)
            if request.META['HTTP_REFERER']:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                return HttpResponseRedirect("/")
        else:
            return render(request, 'index.html', {'erros': 'true'})
    else:
#        raise Http404
        return HttpResponseRedirect("/")

def Logout(request):
    auth.logout(request)
    if request.META['HTTP_REFERER']:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect("/")

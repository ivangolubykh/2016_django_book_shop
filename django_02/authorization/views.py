from django.contrib import auth

# Create your views here.
from django.shortcuts import render, HttpResponseRedirect
#from django.http import Http404


def Return_to_back(request):
    try:
        referer = request.META['HTTP_REFERER']
    except:
        referer = False
    if referer:
        # if request.path == reverse('login') or request.path == reverse('login'):
        if referer == request.build_absolute_uri():
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect(referer)
    else:
        return HttpResponseRedirect("/")


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
#        if user is not None:
        if user:
            auth.login(request, user)
            if not request.POST.get('save'):
                request.session.set_expiry(0)
            return Return_to_back(request)
        else:
            return render(request, 'index.html', {'erros': 'true'})
    else:
#        raise Http404
        return Return_to_back(request)


def Logout(request):
    if request.method == "POST" and request.user.is_authenticated:
        auth.logout(request)
    return Return_to_back(request)

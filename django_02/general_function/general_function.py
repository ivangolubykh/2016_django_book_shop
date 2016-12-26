from django.shortcuts import render, HttpResponseRedirect
#from django.core.urlresolvers import reverse
#from django.http import HttpResponse


def Return_to_back(request):
    if request.META['HTTP_REFERER']:
        # if request.path == reverse('login') or request.path == reverse('login'):
        if request.META['HTTP_REFERER'] == request.build_absolute_uri():
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect("/")


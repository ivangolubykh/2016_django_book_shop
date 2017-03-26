from django.shortcuts import render, HttpResponseRedirect
# from django.core.urlresolvers import reverse
# from django.http import HttpResponse


def Return_to_back(request):
    try:
        referer = request.META['HTTP_REFERER']
    except:
        referer = False
    if referer:
        # if request.path == reverse('login') or
        #     request.path == reverse('login'):
        if referer == request.build_absolute_uri():
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect(referer)
    else:
        return HttpResponseRedirect("/")

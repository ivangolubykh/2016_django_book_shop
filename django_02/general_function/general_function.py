from django.shortcuts import render, HttpResponseRedirect


def Return_to_back(request):
    if request.META['HTTP_REFERER']:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect("/")

from django.shortcuts import render

# Create your views here.
from .forms import Add_User_Form
from general_function.general_function import Return_to_back

def Main(request):
    return render(request, 'index.html')

def Reguster_User(request):
    if request.method == 'POST':
        form = Add_User_Form(request.POST)
        if form.is_valid():
            form.save()
            return Return_to_back(request)
        context = {'form': form}
        return render(request, 'register_user.html', context)
    context = {'form': Add_User_Form()}
    return render(request, 'register_user.html', context)

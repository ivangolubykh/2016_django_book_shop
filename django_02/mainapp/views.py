from django.shortcuts import render

from administrations.forms import Add_User_Form, Edit_Book_Author
from general_function.general_function import Return_to_back
from .models import Books_Author


def Main(request):
    return render(request, 'index.html')

def Register_User(request):
    if request.method == 'POST':
        form = Add_User_Form(request.POST)
        if form.is_valid():
            form.save()
            return Return_to_back(request)
        context = {'form': form}
        return render(request, 'register_user.html', context)
    context = {'form': Add_User_Form()}
    return render(request, 'register_user.html', context)



def List_Books(request, booknumber):
    return render(request, 'administrations/adminn_books_authors.html')

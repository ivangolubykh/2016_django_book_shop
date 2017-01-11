from django.shortcuts import render

from admin_users.forms import Add_User_Form
from general_function.general_function import Return_to_back


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
    return render(request, 'admin_book/adminn_books_authors.html')

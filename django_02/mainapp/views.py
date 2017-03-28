from django.shortcuts import render
from admin_users.forms import Add_User_Form
from general_function.general_function import Return_to_back
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from admin_book.models import Books_Categories, Books


# Список книг на главной с помощью клсасса:
class MainListView(ListView):
    # model = Books_Categories
    queryset = Books_Categories.objects.order_by('bcname').\
        prefetch_related('books_set', 'books_set__bauthor')
    template_name = 'index.html'


class BookDetailView(DetailView):
    # model = Books
    queryset = Books.objects.prefetch_related('bauthor', 'bcategories')
    template_name = 'book.html'


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

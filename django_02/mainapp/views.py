from django.shortcuts import render
from admin_users.forms import Add_User_Form
from general_function.general_function import Return_to_back
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from admin_book.models import Books_Categories, Books
from django.db.models import Q


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


class SearchBookListView(ListView):
    model = Books
    paginate_by = 2
    template_name = 'search.html'

    def get_queryset(self):
        result = super(SearchBookListView, self).get_queryset().\
            order_by('bname')
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            query_list_or = []
            query_list_or.append(Q(bname__icontains=query_list[0]))
            for x in range(1, len(query_list)):
                query_list_or[0] = query_list_or[0] &\
                                   Q(bname__icontains=query_list[x])
            query_list_or.append(Q(bauthor__baauthor__icontains=query_list[0]))
            for x in range(1, len(query_list)):
                query_list_or[1] =\
                    query_list_or[1] &\
                    Q(bauthor__baauthor__icontains=query_list[x])
            result = result.filter(query_list_or[0] | query_list_or[1])
        return result

    def get_context_data(self, **kwargs):
        context = super(SearchBookListView, self).get_context_data(**kwargs)
        context['get_get'] = dict(self.request.GET)
        if self.request.GET.get('q'):
            context['q'] = self.request.GET.get('q')
        return context

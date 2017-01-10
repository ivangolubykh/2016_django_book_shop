from django import forms
from mainapp.models import Books_Categories, Books, Books_Author


class Edit_Book_Author(forms.ModelForm):
    class Meta:
        # Модель (БД) данных, которую используем:
        model = Books_Author
        # Типы полей, отображаемых в форме
        fields = ('__all__')

class Edit_Book_Categories(forms.ModelForm):
    class Meta:
        # Модель (БД) данных, которую используем:
        model = Books_Categories
        # Типы полей, отображаемых в форме
        fields = ('__all__')

class Edit_Books(forms.ModelForm):
    class Meta:
        # Модель (БД) данных, которую используем:
        model = Books
        # Типы полей, отображаемых в форме
        fields = ('__all__')


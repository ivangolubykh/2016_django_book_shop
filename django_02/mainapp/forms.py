from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Add_User_Form(UserCreationForm):
    email = forms.EmailField(required=True, label='E-mail')
    first_name = forms.CharField(required=False, label='Имя')
    last_name = forms.CharField(required=False, label='Фамилия')

    class Meta:
        # Модель (БД) данных, которую используем:
        model = User
        # Типы полей, отображаемых в форме и их порядок отображения в браузере  (поля 'password1', 'password2' и те, что созданв в этом классе выше - есть всегда); поля 'username' и 'email' встроенные:
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super(Add_User_Form, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
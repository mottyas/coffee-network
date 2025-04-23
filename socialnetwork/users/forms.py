from django.forms import ModelForm, TextInput, DateInput, Textarea, FileInput
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'gender', 'city', 'birth_date', 'status')


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', required=True)
    first_name = forms.CharField(label='Имя', required=True)
    last_name = forms.CharField(label='Фамилия', required=True)

    error_messages = {
        'duplicate_username': "Пользователь с таким именем уже существует",
        'password_mismatch': "Введенные пароли не совпадают",
    }

    field_order = ['username', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = 'Может содержать только буквы, цифры и символы @ . + - _'
        self.fields['password1'].help_text = """
        Пароль не может быть похож на имя пользователя.

        Пароль должен содержать как минимум 8 символов.

        Пароль не должен быть простым и часто используемым.

        Пароль не должен содержать только цифры.
        """
        self.fields['password2'].help_text = 'Для подтверждения введите, пожалуйста, пароль ещё раз.'
        self.fields['username'].widget.attrs['maxlength'] = 20


class EditProfileForm(ModelForm):
    class Meta:
        fields = ['gender', 'city', 'birth_date', 'avatar', 'status']

        widgets = {
            "first_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            "last_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            "gender": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пол'
            }),
            "birth_date": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата рождения'
            }),
            "status": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Статус'
            }),
            "avatar": FileInput()
        }

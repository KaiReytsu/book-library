from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class SignUpForm(UserCreationForm):
    username_regex = RegexValidator(regex='[A-Z][a-z]+[0-9]|[А-ЯЁ][а-яё]+[0-9]')
    username = forms.CharField(validators=[username_regex], max_length=20, widget=forms.TextInput(attrs={'class': 'fadeIn second', 'placeholder': 'Логин'}))
    first_name = forms.CharField(max_length=50)
    last_name=forms.CharField(max_length=50, )
    email=forms.EmailField(max_length=50, widget=forms.TextInput(attrs={'class': 'fadeIn second', 'placeholder': 'Email'}))
    phone_regex = RegexValidator(regex=r'(\+[7])|[8]\(?\d{3}\)?(((\d\-?){5,8})|((\d\ ?){7,8}))\d$', message="Phone number must be entered in the format: '+7(999)9999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=14, label='Номер телефона')
    password1=forms.CharField(widget=forms.TextInput(attrs={'class': 'fadeIn second', 'placeholder': 'Пароль'}))
    password2=forms.CharField(widget=forms.TextInput(attrs={'class': 'fadeIn second', 'placeholder': 'Повторите пароль'}))
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'fadeIn second', 'id': 'login', 'name': 'login', 'placeholder': 'Логин'}))
    password = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'fadeIn third', 'id': 'password', 'name': 'login', 'placeholder': 'Пароль'})
    )
    class Meta():
        model = User
        fields = ['username', 'password']
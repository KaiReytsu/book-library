from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class SignUpForm(UserCreationForm):
    username_regex = RegexValidator(regex='[a-zA-Z]+[0-9]*|[а-яёА-ЯЁ]+[0-9]*')
    username = forms.CharField(
        validators=[username_regex], 
        max_length=20, 
        widget=forms.TextInput(
            attrs={
                    'class': 'fadeIn second', 
                    'placeholder': 'Логин'}), 
        help_text='Логин может содержать латинские буквы или кирилицу, а так же цифры')
    email=forms.EmailField(
        max_length=50, 
        widget=forms.TextInput(
            attrs={
                    'class': 'fadeIn second', 
                    'placeholder': 'Email'}),
        help_text='Email формата name@name.com')
    password1=forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                    'class': 'fadeIn third', 
                    'placeholder': 'Пароль'}))
    password2=forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                    'class': 'fadeIn third', 
                    'placeholder': 'Повторите пароль'}),
        help_text='Повторите введенный выше пароль')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'fadeIn second', 'id': 'login', 'name': 'login', 'placeholder': 'Логин'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'fadeIn third', 'id': 'password', 'name': 'login', 'placeholder': 'Пароль'})
    )
    class Meta():
        model = User
        fields = ['username', 'password']
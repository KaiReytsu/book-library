from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class SignUpForm(UserCreationForm):
    username_regex_name = RegexValidator(
        regex='[a-zA-Z]+|[а-яёА-ЯЁ]+', 
        message='Логин должен содержать латинские буквы или кирилицу')
    username_regex_len = RegexValidator(
        regex='([a-zA-Z]*|[а-яёА-ЯЁ]*){3,21}', 
        message='Минимальная длина логина должна быть не менее 3 символов')
    username = forms.CharField(
        validators=[username_regex_name, username_regex_len],
        label='',
        max_length=20, 
        widget=forms.TextInput(
            attrs={
                    'class': 'fadeIn second', 
                    'placeholder': 'Логин'}))
    email=forms.EmailField(
        max_length=50,
        label='',
        widget=forms.TextInput(
            attrs={
                    'class': 'fadeIn second', 
                    'placeholder': 'Email'}))
    password1=forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                    'class': 'fadeIn third', 
                    'placeholder': 'Пароль'}),
        label='')
    password2=forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                    'class': 'fadeIn third', 
                    'placeholder': 'Повторите пароль'}),
        label='')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')  
        lowercase_username = username.lower()         

        return lowercase_username

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=20,
        label='',
        widget=forms.TextInput(
            attrs={
                    'class': 'fadeIn second', 
                    'id': 'login', 
                    'name': 'login', 
                    'placeholder': 'Логин'}))
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                    'class': 'fadeIn third', 
                    'id': 'password', 
                    'name': 'login', 
                    'placeholder': 'Пароль'})
    )
    class Meta():
        model = User
        fields = ['username', 'password']

    # first_name = forms.CharField(max_length=50)
    # last_name=forms.CharField(max_length=50)
    # phone_regex = RegexValidator(regex=r'(\+[7])|[8]\(?\d{3,4}\)?(((\d\-?){5,8})|((\d\ ?){7,8}))\d$', message="Номер телефона должен быть в формате: '+7(999)9999999'")
    # phone_number = forms.CharField(validators=[phone_regex], max_length=14, label='Номер телефона')
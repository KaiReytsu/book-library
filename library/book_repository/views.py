from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginForm, SignUpForm


class SignUp(SuccessMessageMixin, CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'library/registration.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        send_mail(
            subject='Успешная регистрация в библиотеке',
            message='Добро пожаловать на сайт библиотеки. Надеюсь Вый найдёте книги Вам по вкусу',
            from_email='kai.reytsu@yandex.ru',
            recipient_list=[email],
        )
        email_sent = super(SignUp, self).form_valid(form)
        return email_sent
    
class LogIn(LoginView):
    form_class = LoginForm
    template_name = 'library/login.html'

class UserLogout(LogoutView):
    template_name = 'base.html'

def user_page(request):
    return render(request, 'library/user_page.html')
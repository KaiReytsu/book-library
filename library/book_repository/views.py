from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.detail import DetailView

from .forms import LoginForm, SignUpForm
from .models import Book, Genre


class SignUp(SuccessMessageMixin, CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'library/registration.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        send_mail(
            subject='Успешная регистрация в библиотеке',
            message='Добро пожаловать на сайт библиотеки. Надеюсь Вы найдёте книги Вам по вкусу',
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

class BookList(ListView):
    model = Book
    template_name = 'library/book_list.html'
    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q')
        data = super().get_context_data(**kwargs)
        if query:
            book_name_list = Book.objects.filter(
                Q(book_name__icontains=query))
            author_name_list = Book.objects.filter(
                Q(author__author_name__icontains=query))
            genre_name_list = Book.objects.filter(
                Q(genre__genre_name__icontains=query)
             )
            data['book_list'] = book_name_list | author_name_list | genre_name_list
            description = None
            if len(genre_name_list) == 1:
                description = Genre.objects.filter(
                    Q(genre_name__icontains= query))
            data['description'] = description
        else:
            data['book_list'] = Book.objects.all()
        return data

class BookDetail(DetailView):
    model = Book
    template_name = 'library/bookdetail.html'

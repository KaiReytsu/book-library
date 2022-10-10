import json
from datetime import datetime, timedelta, date

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .forms import LoginForm, ReservationForm, SignUpForm
from .models import Author, Book, Genre, Reservation


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
    template_name = 'library/logout.html'

class UserView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'login/'
    model= Reservation
    template_name = 'library/user_page.html'
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['reservation'] = Reservation.objects.filter(Q(user = self.request.user.id)).order_by('date_of_issue')
        return data
    def post(self, request, *args, **kwargs):
        data = request.body.decode('utf-8')
        js_data = json.loads(data)
        reservation = Reservation.objects.filter(id = js_data['id']).first()
        if reservation.user.id == self.request.user.id:
            reservation.delete()
            book = Book.objects.filter(id = reservation.book.id).first()
            book.books_in_stock = book.books_in_stock + 1
            book.save()

class BookList(ListView):
    model = Book
    template_name = 'library/book_list.html'
    # TODO: пагинация для поиска
    paginate_by = 6
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
            data['book_list'] = (book_name_list | author_name_list | genre_name_list).order_by('id').distinct('id')
            
            description = None
            if len(genre_name_list) == 1:
                description = Genre.objects.filter(
                    Q(genre_name__icontains= query))
            data['description'] = description
        return data

class BookDetail(DetailView):
    model = Book
    template_name = 'library/bookdetail.html'


class ReservationView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = ReservationForm
    model = Reservation
    template_name = 'library/reservationpage.html'
    def post(self, request, *args, **kwargs):
        # TODO:Бронирование только авторизованными пользователями
        data = request.body.decode('utf-8')
        date = json.loads(data)
        book = Book.objects.filter(id = date['book_id']).first()
        if len(Reservation.objects.filter(user = request.user, book = book).filter(~Q(status = Reservation.Status.CLOSED))) > 0:
            js_data = {'res_status': 'not closed'}
            return JsonResponse(js_data)
        reservation = Reservation()
        reservation.book = book
        reservation.date_of_issue = date['date_of_issue']
        date_of_return = datetime.strptime(reservation.date_of_issue, '%Y-%m-%dT%H:%M:%S.%f%z')+ timedelta(days=10)
        reservation.date_of_return = date_of_return
        reservation.user = request.user
        reservation.save()
        book.books_in_stock = book.books_in_stock - 1
        book.save()
        js_data = {'reservation_id': reservation.hash, 'reservation_date_of_return': reservation.date_of_return.date()}
        return JsonResponse(js_data)

def start_page(request):
    book_count = Book.objects.all().count()
    author_count = Author.objects.all().count()
    book = Book.objects.filter(id = book_count)
    genres = Genre.objects.all()
    context = {
                'book': book, 
                'list_book': book_count,
                'list_author': author_count,
                'genres': genres
                }
    return render(request, template_name='base.html', context=context)


from book_repository import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', views.main_page, name='mainpage'),
    path('', views.UserLogout.as_view(), name='mainpage'),
    path('login/', views.LogIn.as_view(), name='login'),
    path('registration/', views.SignUp.as_view(), name='registration'),
    path('user/', views.user_page, name='user'),
]

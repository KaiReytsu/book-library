from book_repository import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.UserLogout.as_view(), name='mainpage'),
    path('login/', views.LogIn.as_view(), name='login'),
    path('registration/', views.SignUp.as_view(), name='registration'),
    #path('profile/<slug:username>/', views.UserProfileView.as_view(), name='user'),
]

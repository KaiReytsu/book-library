from book_repository import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('', views.start_page, name='mainpage'),
    path('login/', views.LogIn.as_view(), name='login'),
    path('registration/', views.SignUp.as_view(), name='registration'),
    path('catalog/', views.BookList.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetail.as_view(), name='bookdetail'),
    path('profile/', views.UserView.as_view(), name='user'),
    path('reservation/', views.ReservationView.as_view(), name='reservation'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


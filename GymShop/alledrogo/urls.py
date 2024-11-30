from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, login, register, profile, logout, produkt_detail
from . import views
urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('produkt/<int:id>/', produkt_detail, name='produkt_detail'),
    path('koszyk/', views.koszyk, name='koszyk'),
    path('koszyk/dodaj/<int:produkt_id>/', views.dodaj_do_koszyka, name='dodaj_do_koszyka'),
    path('koszyk/update/<int:pozycja_id>/', views.update_pozycja_koszyka, name='update_pozycja_koszyka'),
    path('koszyk/remove/<int:pozycja_id>/', views.remove_item_from_cart, name='remove_item_from_cart'),
    path('zamowienie/', views.zamowienie, name='zamowienie'),
    path('zamowienia/', views.zamowienia, name='zamowienia'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
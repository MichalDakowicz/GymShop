from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, login, register, profile, logout, produkt_detail

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('produkt/<int:id>/', produkt_detail, name='produkt_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
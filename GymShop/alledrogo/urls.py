from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, login, register, profile, logout

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
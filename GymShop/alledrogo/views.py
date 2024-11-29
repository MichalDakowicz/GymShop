from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .forms import CustomLoginForm, CustomRegisterForm
from .models import Produkt, Kategoria, Koszyk,PozycjaKoszyka
from django.http import HttpResponse, JsonResponse
from django.db.models import F


def remove_item_from_cart(request, pozycja_id):
    pozycja = get_object_or_404(PozycjaKoszyka, id=pozycja_id)
    pozycja.delete()
    return redirect('koszyk')


def update_pozycja_koszyka(request, pozycja_id):
    if request.method == 'POST':
        pozycja = get_object_or_404(PozycjaKoszyka, id=pozycja_id)
        # Pobieramy ilość z formularza (może być ręcznie wpisana lub zmieniona)
        ilosc = int(request.POST.get('ilosc', pozycja.ilosc))

        if ilosc <= 0:
            pozycja.delete()  # Jeśli ilość <= 0, usuwamy produkt z koszyka
        else:
            pozycja.ilosc = ilosc
            pozycja.save()

    return redirect('koszyk')

def home(request):
    produkty = Produkt.objects.all()
    return render(request, 'home.html', {'produkty': produkty})

def produkt_detail(request, id):
    produkt = get_object_or_404(Produkt, id=id)
    return render(request, 'produkt_detail.html', {'produkt': produkt})

def kategoria(request, id):
    kategoria_user = Kategoria.objects.get(pk=id)
    return HttpResponse(kategoria_user.nazwa)

def login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username_or_email, password=password)
            if user is None:
                try:
                    username = User.objects.get(email=username_or_email).username
                    user = authenticate(request, username=username, password=password)
                except User.DoesNotExist:
                    pass
            if user is not None:
                auth_login(request, user)
                return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomRegisterForm()
    return render(request, 'register.html', {'form': form})

def profile(request):
    return render(request, 'profile.html')

def logout(request):
    auth_logout(request)
    return redirect('home')




def dodaj_do_koszyka(request, produkt_id):
    produkt = get_object_or_404(Produkt, id=produkt_id)
    koszyk, created = Koszyk.objects.get_or_create(klient=request.user)


    ilosc = int(request.POST.get('quantity', 1))


    koszyk_produkt, created = KoszykProdukt.objects.get_or_create(koszyk=koszyk, produkt=produkt)
    if not created:
        koszyk_produkt.ilosc += ilosc
    else:
        koszyk_produkt.ilosc = ilosc
    koszyk_produkt.save()

    return redirect('koszyk')



def dodaj_do_koszyka(request, produkt_id):
    produkt = get_object_or_404(Produkt, id=produkt_id)
    ilosc = int(request.POST.get('quantity', 1))
    koszyk, created = Koszyk.objects.get_or_create(klient=request.user)


    pozycja, created = PozycjaKoszyka.objects.get_or_create(koszyk=koszyk, produkt=produkt)
    if not created:
        pozycja.ilosc = F('ilosc') + ilosc
    else:
        pozycja.ilosc = ilosc
    pozycja.save()

    return redirect('koszyk')


def koszyk(request):
    koszyk, created = Koszyk.objects.get_or_create(klient=request.user)
    pozycje = koszyk.pozycje.select_related('produkt')
    total = sum([pozycja.cena_calosciowa for pozycja in pozycje])
    return render(request, 'koszyk.html', {'pozycje': pozycje, 'total': total})

def home(request):
    # Pobierz wszystkie kategorie
    kategorie = Kategoria.objects.all()

    # Pobierz wartość wybranej kategorii z parametrów GET
    kategoria_id = request.GET.get('kategoria')

    # Filtrowanie produktów według wybranej kategorii
    if kategoria_id:
        produkty = Produkt.objects.filter(kategoria_id=kategoria_id)
    else:
        produkty = Produkt.objects.all()

    context = {
        'produkty': produkty,
        'kategorie': kategorie,
        'wybrana_kategoria': int(kategoria_id) if kategoria_id else None,
    }

    return render(request, 'home.html', context)
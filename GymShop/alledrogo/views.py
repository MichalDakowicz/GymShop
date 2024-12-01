from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .forms import CustomLoginForm, CustomRegisterForm, CompanyRegisterForm, ZamowienieForm
from .models import Produkt, Kategoria, Koszyk, PozycjaKoszyka, Firma, Zamowienie, PozycjaZamowienia
from django.http import HttpResponse, JsonResponse
from django.db.models import F, Q, Avg  # Import F, Q, Avg
from django.utils import timezone  # Import timezone
from datetime import timedelta
from .models import Ocena  # Import Ocena model

def register(request):
    if request.method == 'POST':
        user_form = CustomRegisterForm(request.POST)
        company_form = CompanyRegisterForm(request.POST, request.FILES)

        if user_form.is_valid() and company_form.is_valid():
            user = user_form.save()
            user.set_password(user_form.cleaned_data["password"])
            user.save()

            # Create company profile if it's part of the registration
            firma = company_form.save(commit=False)
            firma.user = user
            firma.save()

            auth_login(request, user)
            return redirect('home')
    else:
        user_form = CustomRegisterForm()
        company_form = CompanyRegisterForm()

    return render(request, 'register.html', {'user_form': user_form, 'company_form': company_form})


def remove_item_from_cart(request, pozycja_id):
    pozycja = get_object_or_404(PozycjaKoszyka, id=pozycja_id)
    pozycja.delete()
    return redirect('koszyk')

def company_profile(request):
    firma = Firma.objects.get(user=request.user)
    return render(request, 'company_profile.html', {'firma': firma})


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
    # Pobierz wszystkie kategorie i firmy
    kategorie = Kategoria.objects.all()
    firmy = Firma.objects.all()

    # Pobierz wszystkie produkty
    produkty = Produkt.objects.all()

    # Wyszukiwanie po nazwie produktu, kategorii i firmie
    search_query = request.GET.get('search', '')
    if search_query:
        produkty = produkty.filter(
            Q(nazwa__icontains=search_query) |
            Q(kategoria__nazwa__icontains=search_query) |
            Q(firma__nazwa__icontains=search_query)
        )

    # Filtracja po kategorii
    wybrana_kategoria_id = request.GET.get('kategoria')
    if wybrana_kategoria_id:
        produkty = produkty.filter(kategoria_id=wybrana_kategoria_id)

    # Filtracja po firmie
    wybrana_firma_id = request.GET.get('firma')
    if wybrana_firma_id:
        produkty = produkty.filter(firma_id=wybrana_firma_id)

    # Sortowanie po cenie
    sortowanie = request.GET.get('sortowanie', 'cena_rosnaco')  # domyślnie rosnąco
    if sortowanie == 'cena_rosnaco':
        produkty = produkty.order_by('cena')
    elif sortowanie == 'cena_malejaco':
        produkty = produkty.order_by('-cena')

    # Filtracja po przedziale cenowym
    cena_min = request.GET.get('cena_min')
    cena_max = request.GET.get('cena_max')

    if cena_min:
        produkty = produkty.filter(cena__gte=float(cena_min))  # Cena >= cena_min
    if cena_max:
        produkty = produkty.filter(cena__lte=float(cena_max))  # Cena <= cena_max

    context = {
        'produkty': produkty,
        'kategorie': kategorie,
        'firmy': firmy,
        'wybrana_kategoria': wybrana_kategoria_id,
        'wybrana_firma': wybrana_firma_id,
        'sortowanie': sortowanie,
        'cena_min': cena_min,
        'cena_max': cena_max,
        'search_query': search_query,
    }

    return render(request, 'home.html', context)

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
    total = sum([pozycja.cena_calosciowa for pozycja in pozycje])  # Fix variable name
    return render(request, 'koszyk.html', {'pozycje': pozycje, 'total': total})

def zamowienie(request):
    koszyk, created = Koszyk.objects.get_or_create(klient=request.user)
    pozycje = koszyk.pozycje.select_related('produkt')
    total = round(sum([pozycja.cena_calosciowa for pozycja in pozycje]), 2)
    
    if not pozycje.exists():
        return redirect('koszyk')  # Redirect to basket if it's empty
    
    if request.method == 'POST':
        form = ZamowienieForm(request.POST)
        if form.is_valid():
            zamowienie = Zamowienie.objects.create(
                klient=request.user,
                imie=form.cleaned_data['imie'],
                nazwisko=form.cleaned_data['nazwisko'],
                ulica=form.cleaned_data['ulica'],
                miasto=form.cleaned_data['miasto'],
                kod_pocztowy=form.cleaned_data['kod_pocztowy'],
                numer_telefonu=form.cleaned_data['numer_telefonu'],
                notatki=form.cleaned_data['notatki'],
                data_dostarczenia=timezone.now() + timezone.timedelta(days=7)
            )
            for pozycja in koszyk.pozycje.all():
                PozycjaZamowienia.objects.create(
                    zamowienie=zamowienie,
                    produkt=pozycja.produkt,
                    ilosc=pozycja.ilosc
                )
            koszyk.delete()
            return redirect('orders')
    else:
        form = ZamowienieForm()
    
    return render(request, 'zamowienie.html', {'form': form, 'koszyk': koszyk, 'total': total})

def zamowienia(request):
    zamowienia = Zamowienie.objects.filter(klient=request.user)
    return render(request, 'orders.html', {'zamowienia': zamowienia})

from django.shortcuts import render, get_object_or_404
from .models import Zamowienie, PozycjaZamowienia

def orders_view(request):
    zamowienia = Zamowienie.objects.filter(user=request.user)
    context = {
        'zamowienia': zamowienia
    }
    return render(request, 'orders.html', context)

def produkt_detail_view(request, produkt_id):
    produkt = get_object_or_404(Produkt, id=produkt_id)
    if request.method == 'POST':
        ocena = int(request.POST.get('ocena'))
        komentarz = request.POST.get('komentarz')
        Ocena.objects.create(produkt=produkt, klient=request.user, ocena=ocena, komentarz=komentarz)
        # Update product's average rating
        produkt.srednia_ocen = Ocena.objects.filter(produkt=produkt).aggregate(Avg('ocena'))['ocena__avg']
        produkt.save()
    oceny = Ocena.objects.filter(produkt=produkt)
    context = {
        'produkt': produkt,
        'oceny': oceny
    }
    return render(request, 'produkt_detail.html', context)

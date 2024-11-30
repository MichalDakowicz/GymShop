from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .forms import CustomLoginForm, CustomRegisterForm, CompanyRegisterForm, ZamowienieForm
from .models import Produkt, Kategoria, Koszyk,PozycjaKoszyka,Firma, Zamowienie
from django.http import HttpResponse, JsonResponse
from django.db.models import F
from django.utils.timezone import now
from datetime import timedelta


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


from django.shortcuts import render
from .models import Produkt, Kategoria

def home(request):
    # Pobierz wszystkie kategorie
    kategorie = Kategoria.objects.all()

    # Pobierz wszystkie produkty
    produkty = Produkt.objects.all()

    # Wyszukiwanie po nazwie produktu
    search_query = request.GET.get('search', '')
    if search_query:
        produkty = produkty.filter(nazwa__icontains=search_query)  # Filtracja na podstawie nazwy produktu

    # Filtracja po kategorii
    wybrana_kategoria_id = request.GET.get('kategoria')
    if wybrana_kategoria_id:
        produkty = produkty.filter(kategoria_id=wybrana_kategoria_id)

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
        'wybrana_kategoria': wybrana_kategoria_id,
        'sortowanie': sortowanie,
        'cena_min': cena_min,
        'cena_max': cena_max,
        'search_query': search_query,
    }

    return render(request, 'home.html', context)

def zamowienie(request):
    if request.method == 'POST':
        # Pobranie koszyka użytkownika
        koszyk = get_object_or_404(Koszyk, klient=request.user)
        pozycje = koszyk.pozycje.select_related('produkt')

        if not pozycje.exists():
            return redirect('koszyk')  # Jeśli koszyk jest pusty, przekierowanie do koszyka

        # Tworzenie nowego zamówienia
        form = ZamowienieForm(request.POST)
        if form.is_valid():
            zamowienie = Zamowienie.objects.create(
                klient=request.user,
                data_dostarczenia=now() + timedelta(days=3),  # Ustawienie daty dostarczenia na 3 dni
                imie=form.cleaned_data['imie'],
                nazwisko=form.cleaned_data['nazwisko'],
                ulica=form.cleaned_data['ulica'],
                miasto=form.cleaned_data['miasto'],
                kod_pocztowy=form.cleaned_data['kod_pocztowy'],
                numer_telefonu=form.cleaned_data['numer_telefonu'],
                notatki=form.cleaned_data['notatki'],
            )

            # Przypisanie produktów do zamówienia
            for pozycja in pozycje:
                zamowienie.produkty.add(pozycja.produkt)
                pozycja.delete()  # Usuwamy produkt z koszyka po złożeniu zamówienia

            zamowienie.save()

            return redirect('home')  # Po zakończeniu zamówienia, przekierowanie na stronę główną
    else:
        form = ZamowienieForm()

    # Pobieramy koszyk użytkownika
    koszyk = get_object_or_404(Koszyk, klient=request.user)
    pozycje = koszyk.pozycje.select_related('produkt')
    total = sum([pozycja.cena_calosciowa for pozycja in pozycje])

    return render(request, 'zamowienie.html', {'form': form, 'koszyk': koszyk, 'total': total})

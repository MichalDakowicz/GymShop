from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Firma,Produkt

class ProduktForm(forms.ModelForm):
    class Meta:
        model = Produkt
        fields = ['nazwa', 'opis', 'cena', 'kategoria', 'zdjecie']
        widgets = {
            'nazwa': forms.TextInput(attrs={'class': 'form-control'}),
            'opis': forms.Textarea(attrs={'class': 'form-control'}),
            'cena': forms.NumberInput(attrs={'class': 'form-control'}),
            'kategoria': forms.Select(attrs={'class': 'form-control'}),
            'zdjecie': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class FirmLoginForm(AuthenticationForm):
    username = forms.CharField(label="Nazwa użytkownika lub email", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ZamowienieForm(forms.Form):
    imie = forms.CharField(max_length=100, label='Imię', required=True)
    nazwisko = forms.CharField(max_length=100, label='Nazwisko', required=True)
    ulica = forms.CharField(max_length=255, label='Ulica', required=True)
    miasto = forms.CharField(max_length=100, label='Miasto', required=True)
    kod_pocztowy = forms.CharField(max_length=10, label='Kod pocztowy', required=True)
    numer_telefonu = forms.CharField(max_length=15, label='Numer telefonu', required=True)
    notatki = forms.CharField(widget=forms.Textarea, label='Dodatkowe notatki', required=False)
    metoda_platnosci = forms.ChoiceField(
        choices=[('credit_card', 'Karta kredytowa'), ('paypal', 'PayPal')],
        label='Metoda płatności',
        required=True
    )

class CustomUserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label="Adres email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Imię", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Nazwisko", widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(
        label="Nazwa użytkownika",
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': 40, 'placeholder': 'Nazwa użytkownika'}),
        help_text="Maksymalnie 40 znaków. Tylko litery, cyfry i @/./+/-/_."
    )
    password1 = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Twoje hasło musi zawierać co najmniej 8 znaków, nie może być powszechnie używanym hasłem ani składać się wyłącznie z cyfr."
    )
    password2 = forms.CharField(
        label="Potwierdzenie hasła",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Wprowadź to samo hasło co wcześniej, w celu weryfikacji."
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class CompanyRegisterForm(forms.ModelForm):
    class Meta:
        model = Firma
        fields = ['nazwa', 'opis', 'ikona']

    ikona = forms.ImageField(required=False)
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Adres email lub nazwa użytkownika", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Adres email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Imię", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Nazwisko", widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(
        label="Nazwa użytkownika",
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': 40, 'placeholder': 'Nazwa użytkownika'}),
        help_text="Maksymalnie 40 znaków. Tylko litery, cyfry i @/./+/-/_."
    )
    password1 = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Twoje hasło musi zawierać co najmniej 8 znaków, nie może być powszechnie używanym hasłem ani składać się wyłącznie z cyfr."
    )
    password2 = forms.CharField(
        label="Potwierdzenie hasła",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Wprowadź to samo hasło co wcześniej, w celu weryfikacji."
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
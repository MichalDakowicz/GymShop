from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

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
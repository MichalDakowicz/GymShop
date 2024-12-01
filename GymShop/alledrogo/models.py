from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg  # Import Avg for calculating average rating

class Firma(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=256)
    opis = models.TextField()
    ikona = models.ImageField(upload_to='media/ikony_firm', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='firma', null=True, blank=True)

    def __str__(self):
        return self.nazwa

class Kategoria(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=256)
    opis = models.TextField()

    def __str__(self):
        return self.nazwa

class Produkt(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=256)
    opis = models.TextField()
    cena = models.FloatField()

    srednia_ocen = models.FloatField(default=0)
    kategoria = models.ForeignKey(Kategoria, on_delete=models.CASCADE)
    firma = models.ForeignKey(Firma, on_delete=models.CASCADE, null=True, blank=True)
    zdjecie = models.ImageField(upload_to='media/zdjecia_produktow', null=True, blank=True)

    def __str__(self):
        return self.nazwa

class Zamowienie(models.Model):
    id = models.AutoField(primary_key=True)
    produkty_z_iloscia = models.ManyToManyField(Produkt, through='PozycjaZamowienia', related_name='zamowienia_z_iloscia')
    klient = models.ForeignKey(User, on_delete=models.CASCADE)
    data_zamowienia = models.DateTimeField(auto_now_add=True)
    data_dostarczenia = models.DateTimeField()
    imie = models.CharField(max_length=100, default='brak')
    nazwisko = models.CharField(max_length=100, default='brak')
    ulica = models.CharField(max_length=255, default='brak')
    miasto = models.CharField(max_length=100, default='brak')
    kod_pocztowy = models.CharField(max_length=6, default='brak')
    numer_telefonu = models.CharField(max_length=15, default='brak')
    notatki = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.klient} - {self.data_zamowienia}'

class Ocena(models.Model):
    id = models.AutoField(primary_key=True)
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE)
    klient = models.ForeignKey(User, on_delete=models.CASCADE)
    ocena = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    komentarz = models.TextField()

    def __str__(self):
        return str(self.produkt) + ' ' + str(self.ocena) + ' ' + str(self.komentarz)

class Koszyk(models.Model):
    id = models.AutoField(primary_key=True)
    klient = models.ForeignKey(User, on_delete=models.CASCADE)
    data_utworzenia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.klient) + ' ' + str(self.data_utworzenia)

class PozycjaKoszyka(models.Model):
    koszyk = models.ForeignKey(Koszyk, on_delete=models.CASCADE, related_name='pozycje')
    produkt = models.ForeignKey('Produkt', on_delete=models.CASCADE)
    ilosc = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.produkt.nazwa} x {self.ilosc}"

    @property
    def cena_calosciowa(self):

        return round(self.produkt.cena * self.ilosc, 2)

class PozycjaZamowienia(models.Model):
    zamowienie = models.ForeignKey(Zamowienie, on_delete=models.CASCADE)
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE)
    ilosc = models.PositiveIntegerField(default=1)

    def cena_calosciowa(self):
        return self.ilosc * self.produkt.cena
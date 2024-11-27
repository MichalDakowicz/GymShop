from django.db import models
from django.contrib.auth.models import User

class Firma(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=256)
    opis = models.TextField()
    ikona = models.ImageField(upload_to='media/ikony_firm', null=True, blank=True)

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
    produkty = models.ManyToManyField(Produkt)
    klient = models.ForeignKey(User, on_delete=models.CASCADE)
    data_zamowienia = models.DateTimeField(auto_now_add=True)
    data_dostarczenia = models.DateTimeField()
    adres_dostawy = models.TextField()

    def __str__(self):
        return str(self.klient) + ' ' + str(self.data_zamowienia)

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
    produkty = models.ManyToManyField(Produkt)
    data_utworzenia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.klient) + ' ' + str(self.data_utworzenia)
from django.db import models
# Create your models here.

class Firma(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=256)
    opis = models.TextField()
    ikona = models.ImageField(upload_to='media/ikony_firm', default=None)
    
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
    kategoria = models.ForeignKey(Kategoria, on_delete=models.CASCADE)
    firma = models.ForeignKey(Firma, on_delete=models.CASCADE, default=None)
    zdjecie = models.ImageField(upload_to='media/zdjecia_produktow', default=None)
    
    def __str__(self):
        return self.nazwa
    
class Klient(models.Model):
    id = models.AutoField(primary_key=True)
    imie = models.CharField(max_length=256)
    nazwisko = models.CharField(max_length=256, default=None)
    email = models.EmailField()
    haslo = models.CharField(max_length=256)
    telefon = models.CharField(max_length=256, default=None)
    
    def __str__(self):
        return self.imie + ' ' + self.nazwisko
    
class Zamowienie(models.Model):
    id = models.AutoField(primary_key=True)
    produkty = models.ManyToManyField(Produkt)
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    data_zamowienia = models.DateTimeField(auto_now_add=True)
    data_dostarczenia = models.DateTimeField()
    adres_dostawy = models.TextField()
   
    def __str__(self): 
        return str(self.klient) + ' ' + str(self.data_zamowienia)
    
class Ocena(models.Model):
    id = models.AutoField(primary_key=True)
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE)
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    ocena = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    komentarz = models.TextField()
    
    def __str__(self):
        return str(self.produkt) + ' ' + str(self.ocena) + ' ' + str(self.komentarz)
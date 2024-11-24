from django.contrib import admin
from .models import Firma, Kategoria, Produkt, Zamowienie, Ocena

# Register your models here.
admin.site.register(Firma)
admin.site.register(Kategoria)
admin.site.register(Produkt)
admin.site.register(Zamowienie)
admin.site.register(Ocena)
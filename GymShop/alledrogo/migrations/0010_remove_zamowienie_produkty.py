# Generated by Django 5.1.3 on 2024-12-01 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alledrogo', '0009_pozycjazamowienia_zamowienie_produkty_z_iloscia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zamowienie',
            name='produkty',
        ),
    ]

# Generated by Django 5.1.3 on 2024-11-18 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeszczedrozej', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='klient',
            name='haslo',
            field=models.CharField(default='haslo', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='klient',
            name='nazwisko',
            field=models.CharField(default=None, max_length=256),
        ),
        migrations.AlterField(
            model_name='klient',
            name='telefon',
            field=models.CharField(default=None, max_length=256),
        ),
    ]
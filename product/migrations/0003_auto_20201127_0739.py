# Generated by Django 3.0.7 on 2020-11-27 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20201125_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorylang',
            name='lang',
            field=models.CharField(choices=[('en', 'English'), ('tr', 'Türkçe'), ('ru', 'Pусский'), ('hi', 'हिंदी द्वारा'), ('ar', 'العربية')], max_length=6),
        ),
        migrations.AlterField(
            model_name='productlang',
            name='lang',
            field=models.CharField(choices=[('en', 'English'), ('tr', 'Türkçe'), ('ru', 'Pусский'), ('hi', 'हिंदी द्वारा'), ('ar', 'العربية')], max_length=6),
        ),
    ]
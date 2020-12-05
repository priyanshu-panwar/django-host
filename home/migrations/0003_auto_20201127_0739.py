# Generated by Django 3.0.7 on 2020-11-27 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20201125_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='lang',
            field=models.CharField(blank=True, choices=[('en', 'English'), ('ar', 'العربية')], max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='settinglang',
            name='lang',
            field=models.CharField(choices=[('en', 'English'), ('ar', 'العربية')], max_length=6),
        ),
    ]
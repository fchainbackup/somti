# Generated by Django 4.2.6 on 2023-10-26 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='transaction_type',
            field=models.CharField(default='deposite', max_length=200),
        ),
        migrations.AlterField(
            model_name='deposite',
            name='cryptos',
            field=models.CharField(default='xrp', max_length=7),
        ),
    ]

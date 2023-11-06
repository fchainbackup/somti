# Generated by Django 4.2.6 on 2023-10-29 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposite', '0004_transactions_withdrawal_transact_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposite',
            name='cryptos',
            field=models.CharField(default='XRP', max_length=7),
        ),
        migrations.AlterField(
            model_name='fund_user_wallet_account',
            name='crypto_types',
            field=models.CharField(choices=[('XRP', 'XRP'), ('XLM', 'XLM'), ('ALGO', 'ALGO'), ('ADA', 'ADA')], default='xrp', max_length=7),
        ),
    ]

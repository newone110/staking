# Generated by Django 5.0.6 on 2024-08-27 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stake', '0007_stake_ada_stake_bch_stake_btc_stake_eth_stake_ltc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stake',
            name='duration',
            field=models.CharField(max_length=10),
        ),
    ]

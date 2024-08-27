# Generated by Django 5.0.6 on 2024-08-27 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stake', '0006_userdatabase_stake_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='stake',
            name='ada',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stake',
            name='bch',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stake',
            name='btc',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stake',
            name='eth',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stake',
            name='ltc',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stake',
            name='xlm',
            field=models.BooleanField(default=False),
        ),
    ]

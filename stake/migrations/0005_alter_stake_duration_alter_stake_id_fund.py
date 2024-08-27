# Generated by Django 5.0.6 on 2024-08-25 10:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stake', '0004_auto_20240824_2254'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='stake',
            name='duration',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='stake',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('crypto_asset', models.CharField(default='btc', max_length=255)),
                ('now_id', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('waiting', 'Waiting'), ('confirming', 'Confirming'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected'), ('expired', 'Expired')], default='waiting', max_length=10)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

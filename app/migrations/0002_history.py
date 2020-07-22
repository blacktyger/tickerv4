# Generated by Django 2.2.5 on 2020-07-12 18:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pair', models.CharField(choices=[('usdt', 'usdt'), ('btc', 'btc')], default=('usdt', 'usdt'), max_length=100)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('avg_price', models.CharField(default='0', max_length=124)),
                ('vol_24h', models.CharField(default='0', max_length=124)),
                ('percentage_change_24h', models.CharField(default='0', max_length=124)),
                ('percentage_change_7d', models.CharField(default='0', max_length=124)),
                ('market_cap', models.CharField(default='0', max_length=124)),
                ('ath', models.CharField(default='0', max_length=124)),
                ('ath_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ath_change', models.CharField(default='0', max_length=124)),
                ('explorer', django_extensions.db.fields.json.JSONField(default={})),
                ('last_block', models.DateTimeField(default=django.utils.timezone.now)),
                ('block_value', models.CharField(default='0', max_length=124)),
                ('to_save', models.BooleanField(default=False)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='app.Coin')),
            ],
        ),
    ]
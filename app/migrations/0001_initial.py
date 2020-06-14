# Generated by Django 3.0.7 on 2020-06-14 16:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('symbol', models.CharField(max_length=124, primary_key=True, serialize=False)),
                ('name', models.CharField(default='name', max_length=124)),
                ('links', django_extensions.db.fields.json.JSONField(default={})),
                ('img', models.CharField(default='', max_length=124)),
                ('mw_coin', models.BooleanField(default=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(default='name', max_length=124)),
                ('flag', models.CharField(default='flag', max_length=124)),
                ('country', models.CharField(default='country', max_length=124)),
                ('price', models.CharField(default='price', max_length=124)),
            ],
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('name', models.CharField(max_length=124, primary_key=True, serialize=False)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('year_established', models.CharField(default='2020', max_length=124)),
                ('country', models.CharField(default='-', max_length=124)),
                ('url', models.CharField(default='-', max_length=124)),
                ('image', models.CharField(default='-', max_length=124)),
                ('centralized', models.CharField(default='-', max_length=124)),
                ('trade_volume_24h_btc', models.CharField(default='-', max_length=124)),
                ('description', models.CharField(default='-', max_length=124)),
                ('telegram_url', models.CharField(default='-', max_length=124)),
                ('trade_volume_24h_btc_normalized', models.CharField(default='-', max_length=124)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='name', max_length=124)),
                ('icon', models.CharField(default='icon', max_length=124)),
                ('link', models.CharField(default='link', max_length=124)),
                ('category', models.CharField(default='social', max_length=124)),
            ],
        ),
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('trading_url', models.CharField(default='', max_length=124)),
                ('pair', models.CharField(choices=[('usdt', 'usdt'), ('btc', 'btc')], default=('usdt', 'usdt'), max_length=100)),
                ('last_price', django_extensions.db.fields.json.JSONField(default={})),
                ('last_trade', models.DateTimeField(default=django.utils.timezone.now)),
                ('bid', django_extensions.db.fields.json.JSONField(default={})),
                ('ask', django_extensions.db.fields.json.JSONField(default={})),
                ('spread', django_extensions.db.fields.json.JSONField(default={})),
                ('high', django_extensions.db.fields.json.JSONField(default={})),
                ('low', django_extensions.db.fields.json.JSONField(default={})),
                ('volume', django_extensions.db.fields.json.JSONField(default={})),
                ('orders', django_extensions.db.fields.json.JSONField(default={})),
                ('trades', django_extensions.db.fields.json.JSONField(default={})),
                ('candles', django_extensions.db.fields.json.JSONField(default={})),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Coin')),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticker', to='app.Exchange')),
            ],
        ),
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Epic Pool', max_length=124)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('blocks', django_extensions.db.fields.json.JSONField(default={})),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pool', to='app.Coin')),
            ],
        ),
        migrations.CreateModel(
            name='Explorer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_block', models.DateTimeField(default=django.utils.timezone.now)),
                ('block_value', models.CharField(default='0', max_length=124)),
                ('circulating', models.CharField(default='0', max_length=124)),
                ('height', models.CharField(default='0', max_length=124)),
                ('reward', models.CharField(default='0', max_length=124)),
                ('average_blocktime', models.CharField(default='0', max_length=124)),
                ('totalcoins', models.CharField(default='0', max_length=124)),
                ('target_diff', django_extensions.db.fields.json.JSONField(default={})),
                ('total_diff', django_extensions.db.fields.json.JSONField(default={})),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='explorer', to='app.Coin')),
            ],
        ),
        migrations.CreateModel(
            name='Data',
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
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='app.Coin')),
            ],
        ),
        migrations.CreateModel(
            name='CoinGecko',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('data', django_extensions.db.fields.json.JSONField(default={})),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coingecko', to='app.Coin')),
            ],
        ),
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='-', max_length=124)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('div', models.TextField(default='-')),
                ('script', models.TextField(default='-')),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chart', to='app.Coin')),
            ],
        ),
    ]

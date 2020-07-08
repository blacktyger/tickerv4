from django.db import models
from django.utils import timezone
from django_extensions.db.fields.json import JSONField
from django.utils import timezone
from .globals import pairs
from .tools import *

register = template.Library()

PAIRS = tuple((target, target) for target in pairs)


class Link(models.Model):
    name = models.CharField(max_length=124, default='name')
    icon = models.CharField(max_length=124, default='icon')
    link = models.CharField(max_length=124, default='link')
    category = models.CharField(max_length=124, default='social')


class Currency(models.Model):
    updated = models.DateTimeField(default=timezone.now)
    symbol = models.CharField(max_length=124, default='name')
    flag = models.CharField(max_length=124, default='flag')
    country = models.CharField(max_length=124, default='country')
    price = models.CharField(max_length=124, default='price')
    to_save = models.BooleanField(default=False)


class Exchange(models.Model):
    name = models.CharField(max_length=124, primary_key=True)
    updated = models.DateTimeField(default=timezone.now)
    year_established = models.CharField(max_length=124, default='2020')
    country = models.CharField(max_length=124, default='-')
    url = models.CharField(max_length=124, default='-')
    image = models.CharField(max_length=124, default='-')
    centralized = models.CharField(max_length=124, default='-')
    trade_volume_24h_btc = models.CharField(max_length=124, default='-')
    description = models.CharField(max_length=124, default='-')
    telegram_url = models.CharField(max_length=124, default='-')
    trade_volume_24h_btc_normalized = models.CharField(max_length=124, default='-')
    to_save = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Coin(models.Model):
    symbol = models.CharField(max_length=124, primary_key=True)
    name = models.CharField(max_length=124, default='name')
    links = JSONField(default={})
    img = models.CharField(max_length=124, default='')
    mw_coin = models.BooleanField(default=True, null=True)
    to_save = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pairs = pairs

    def __str__(self):
        return self.symbol


class Data(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='data')
    pair = models.CharField(choices=PAIRS, default=PAIRS[0], max_length=100)

    updated = models.DateTimeField(default=timezone.now)
    avg_price = models.CharField(max_length=124, default='0')
    vol_24h = models.CharField(max_length=124, default='0')
    percentage_change_24h = models.CharField(max_length=124, default='0')
    percentage_change_7d = models.CharField(max_length=124, default='0')
    market_cap = models.CharField(max_length=124, default='0')
    ath = models.CharField(max_length=124, default='0')
    ath_date = models.DateTimeField(default=timezone.now)
    ath_change = models.CharField(max_length=124, default='0')
    explorer = JSONField(default={})
    last_block = models.DateTimeField(default=timezone.now)
    block_value = models.CharField(max_length=124, default='0')
    to_save = models.BooleanField(default=False)

    def market_cap_change_24h(self):
        return change(Data.objects.filter(coin=self.coin, pair=self.pair), 'market_cap')

    def market_avg_price_24h(self):
        return change(Data.objects.filter(coin=self.coin, pair=self.pair), 'avg_price')


class Pool(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='pool')

    name = models.CharField(max_length=124, default="Epic Pool")
    updated = models.DateTimeField(default=timezone.now)
    blocks = JSONField(default={})
    to_save = models.BooleanField(default=False)


class Explorer(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='explorer')

    updated = models.DateTimeField(default=timezone.now)
    last_block = models.DateTimeField(default=timezone.now)
    circulating = models.CharField(max_length=124, default='0')
    height = models.CharField(max_length=124, default='0')
    reward = models.CharField(max_length=124, default='0')
    average_blocktime = models.CharField(max_length=124, default='0')
    totalcoins = models.CharField(max_length=124, default='0')
    target_diff = JSONField(default={})
    total_diff = JSONField(default={})
    to_save = models.BooleanField(default=False)


class Ticker(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='ticker')
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)

    updated = models.DateTimeField(default=timezone.now)
    trading_url = models.CharField(max_length=124, default='')
    pair = models.CharField(choices=PAIRS, default=PAIRS[0], max_length=100)
    last_price = JSONField(default={})
    last_trade = models.DateTimeField(default=timezone.now)
    bid = JSONField(default={})
    ask = JSONField(default={})
    spread = JSONField(default={})
    high = JSONField(default={})
    low = JSONField(default={})
    volume = JSONField(default={})
    orders = JSONField(default={})
    trades = JSONField(default={})
    candles = JSONField(default={})
    to_save = models.BooleanField(default=False)


def get_ticker(coin, exchange, last=False):
    if last:
        return Ticker.objects.filter(coin=coin, exchange=exchange).latest('updated')
    else:
        return Ticker.objects.filter(coin=coin, exchange=exchange)


class CoinGecko(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='coingecko')
    updated = models.DateTimeField(default=timezone.now)

    data = JSONField(default={})
    to_save = models.BooleanField(default=False)


def get_gecko(coin):
    return CoinGecko.objects.filter(coin=coin).latest('updated')


class Chart(models.Model):
    name = models.CharField(max_length=124, default='-')
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='chart')
    updated = models.DateTimeField(default=timezone.now)
    div = models.TextField(default='-')
    script = models.TextField(default='-')
    to_save = models.BooleanField(default=False)


@register.filter()
def usd_to_btc(value):
    """
    Convert amount (value) of USD to BTC.
    """
    return d(value) / d(Coin.objects.get(symbol="BTC").coingecko.latest('updated').data['price'])


@register.filter()
def btc_to_usd(value):
    """
    Convert amount (value) of BTC to USD.
    """
    return d(value) * d(Coin.objects.get(symbol="BTC").coingecko.latest('updated').data['price'])
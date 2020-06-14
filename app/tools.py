import datetime
import statistics
import json
import requests
from django import template
from decimal import Decimal, InvalidOperation
from django.utils.timezone import make_aware
from .models import *

register = template.Library()


def d(value, places=8):
    try:
        return round(Decimal(value), places)
    except InvalidOperation:
        if value == '' or ' ':
            print('Value "" or " "')
            return Decimal(0)
        else:
            print('Value is a string')
            pass


def api(url, query):
    url = url + query
    return json.loads(requests.get(url).content)


def t_s(timestamp):
    """ Convert different timestamps to datetime object"""
    if len(str(timestamp)) == 13:
        time = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
    if len(str(timestamp)) == 10:
        time = datetime.datetime.fromtimestamp(int(timestamp))
    if len(str(timestamp)) == 16:
        time = datetime.datetime.fromtimestamp(int(timestamp / 1000000))
    return make_aware(time)


def fields(model):
    """
    Get model fields names as list of strings.
    """
    return [str(f).split('.')[(-1)] for f in model._meta.get_fields()]


def updater(model, data):
    """
    Update Exchange model fields with data from dict.
    """
    for field in fields(model):
        for key, value in data.items():
            if key == field:
                setattr(model, field, value)
                model.save()


def spread(ask, bid):
    return round(((d(ask) - d(bid)) / d(ask)) * 100, 2)


def avg(numbers):
    return statistics.mean([d(n) for n in list(numbers)])


def get_gecko(coin):
    return CoinGecko.objects.get(coin=coin)


def get_ticker(coin, exchange, last=False):
    if last:
        return Ticker.objects.filter(coin=coin, exchange=exchange).last()
    else:
        return Ticker.objects.filter(coin=coin, exchange=exchange)


def get_flag(country):
    url = f'https://www.countryflags.io/{country}/shiny/64.png'
    return url


@register.filter()
def usd_to_btc(value):
    """
    Convert amount (value) of USD to BTC.
    """
    return d(value) / d(Coin.objects.get(symbol="BTC").coingecko.last().data['price'])


@register.filter()
def btc_to_usd(value):
    """
    Convert amount (value) of BTC to USD.
    """
    return d(value) * d(Coin.objects.get(symbol="BTC").coingecko.last().data['price'])

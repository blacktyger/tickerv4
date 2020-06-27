from datetime import timedelta
from django.utils import timezone
from statistics import mean
from django import template

from app.models import get_gecko, Coin
from app.tools import d, t_s, avg
from app.coins.data import models, filters


register = template.Library()


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


@register.filter(name='check_arrow')
def check_arrow(value):
    if d(value) <= 0:
        return '<i class="fa fa-arrow-down color-red"></i>'
    else:
        return '<i class="fa fa-arrow-up color-green"></i>'


@register.filter(name='check_color')
def check_color(value):
    if d(value) <= 0:
        return 'red'
    else:
        return 'green'


@register.filter
def get_dash(mapping, key):
    return mapping.get(key, '-')


@register.filter()
def minus_back(value, num):
    return d(num) - d(value)


@register.filter()
def add(value, num):
    return d(value) + d(num)


@register.filter()
def times(value, num):
    return d(value) * d(num)


@register.filter()
def get_percent(value, num):
    """
    :param value:
    :param num:
    :return: rounded percentage value of num
    """
    return d(d(value) / d(num) * 100, 2)


@register.filter(name='colour')
def percentage_color(value):
    if value < 20:
        return f"progress-bar-danger"
    elif 20 <= value <= 50:
        return f"progress-bar-warning"
    else:
        return f"progress-bar-success"


@register.filter(name="epic_to")
def epic_to(value, target):
    """
    Convert amount (value) of Epic-Cash to given target - USD or Bitcoin.
    """
    if target == 'btc':
        return round(d(filters()['epic']['data'][target].avg_price) * d(value), 8)
    else:
        return round(d(filters()['epic']['data'][target].avg_price) * d(value), 3)


def daily_mined(coin):
    block_time = d(coin.explorer.last().average_blocktime)
    block_reward = d(coin.explorer.last().reward)
    return {'coins': d((86400 / block_time) * block_reward, 0),
            'blocks': d(86400 / block_time, 0)}


def halving(coin):
    block_time = d(coin.explorer.order_by('updated').last().average_blocktime)
    block_height = d(coin.explorer.order_by('updated').last().height)

    def check_height():
        if block_height < 480_960:
            halving_height = 480_960
        else:
            halving_height = 1_157_760
        return halving_height

    time_left = ((check_height() - block_height) * block_time)
    date = timezone.now() + timedelta(seconds=int(time_left))
    return {'date': date, 'height': check_height()}


def high_low_7d(coin, target=""):
    data = [p for t, p in get_gecko(coin).data['price_7d'+target]]
    return {
        'low': min(data),
        'high': max(data),
        'average': mean(data)
        }




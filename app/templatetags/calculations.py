from django import template

from app.tools import d, t_s, avg, get_gecko
from app.coins.data import models, filters
from statistics import mean


register = template.Library()


@register.filter(name='check_color')
def check_color(value):
    if d(value) <= 0:
        return '<i class="fa fa-caret-down color-red"></i>'
    else:
        return '<i class="fa fa-caret-up color-green"></i>'


@register.filter
def get_dash(mapping, key):
    return mapping.get(key, '-')


@register.filter()
def add(value, num):
    return d(value) + d(num)


@register.filter()
def times(value, num):
    return d(value) * d(num)


@register.filter()
def get_percent(value, num):
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
        return round(d(filters()['epic']['data'][target].last().avg_price) * d(value), 8)
    else:
        return round(d(filters()['epic']['data'][target].last().avg_price) * d(value), 3)


def daily_mined(coin):
    block_time = d(coin.explorer.last().average_blocktime)
    block_reward = d(coin.explorer.last().reward)
    return d((86400 / block_time) * block_reward, 0)


def high_low_7d(coin):
    data = [p for t, p in get_gecko(coin).data['price_7d']]
    return {
        'low': min(data),
        'high': max(data),
        'average': mean(data)
        }

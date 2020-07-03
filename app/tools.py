import datetime
import statistics
import json
import requests
from django import template
from decimal import Decimal, InvalidOperation
from .globals import *

from django.utils import timezone
from django.utils.timezone import make_aware

register = template.Library()


def d(value, places=8):
    try:
        return round(Decimal(value), places)
    except InvalidOperation:
        if value == '' or ' ':
            print(f'{warn_msg} Empty string')
            return Decimal(0)
        else:
            print(f'{warn_msg} String should have numbers only')
            pass


def api(url, query):
    url = url + query
    return json.loads(requests.get(url).content)


def t_s(timestamp):
    """ Convert different timestamps to datetime object"""
    if len(str(timestamp)) == 13:
        time = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
    elif len(str(timestamp)) == 10:
        time = datetime.datetime.fromtimestamp(int(timestamp))
    elif len(str(timestamp)) == 16:
        time = datetime.datetime.fromtimestamp(int(timestamp / 1000000))
    else:
        print(f"{warn_msg} Problems with timestamp: {timestamp}, len: {len(str(timestamp))}")
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


def check_saving(record, interval=60*30):
    if record:
        save = (timezone.now() - record.updated).total_seconds() > interval
        # print(f"found last saved and checking time...")
    else:
        save = True
        print(f"{info_msg} no saved found, save this one")
    return save


def time_delta(end, start=timezone.now()):
    delta = (start - end).total_seconds()
    return delta


def spread(ask, bid):
    return round(((d(ask) - d(bid)) / d(ask)) * 100, 2)


def avg(numbers):
    return statistics.mean([d(n) for n in list(numbers)])


def get_flag(country):
    url = f'https://www.countryflags.io/{country}/shiny/64.png'
    return url


def nearest_date(model_qs, interval=60*60*24):
    """
    Find in model query set :updated fields date that is closest to -x :seconds
    from now and return as datetime object.
    """
    dates = [x.updated for x in model_qs.order_by('updated')]
    the_date = timezone.now() - datetime.timedelta(seconds=interval)
    nearest = min(dates, key=lambda x: abs(x - the_date))
    # print(nearest.strftime('%D/%M/%Y | %H:%M:%S'))
    return nearest


def check_change(v2, v1):
    """
    return: percentage change between two values
    """
    return d(((v2-v1)/abs(v1))*100, 8)


def change(model_qs, field, interval=60*60*24):
    now = model_qs.order_by('updated').last()
    # print(getattr(now, field), now.updated)
    before = [x for x in model_qs
              if x.updated == nearest_date(model_qs, interval=interval)][0]
    # print(getattr(before, field), before.updated)
    # print(check_change(d(getattr(now, field)), d(getattr(before, field))))
    return check_change(d(getattr(now, field)), d(getattr(before, field)))
    # else:
    #     print(f"{warn_msg} no previous update")
    #     return 0


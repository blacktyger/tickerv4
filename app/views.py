from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from rest_framework import viewsets

from .serializers import DataSerializer
from .models import *
from .templatetags.calculations import daily_mined, \
    high_low_7d
from .coins.data import coins, all_coins, filters, \
    all_exchanges, models, EXCHANGES, volumes, links
from .globals import pairs
from .templatetags.calculations import halving


class DataViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Epic Cash data.
    """
    queryset = Data.objects.all().order_by('-updated')[0:2]
    serializer_class = DataSerializer


def index(request):
    mw_data = {coin.symbol: CoinGecko.objects.filter(coin=coin).order_by('updated').last().data
               for coin in all_coins() if coin.mw_coin}

    for chart in Chart.objects.filter(name='mw_chart'):
        if chart.coin.mw_coin:
            mw_data[chart.coin.symbol].update({'chart':
                                                   {'div': chart.div,
                                                    'script': chart.script}})

    exchange_data = {ex: {
        target: ex.ticker.filter(pair=target).order_by('updated').last() for target in pairs
        if ex.ticker.filter(pair=target)} for ex in all_exchanges()}

    context = {
        'coins_list': all_coins(),
        'currency': Currency.objects.all(),
        'halving': halving(models()['epic']),
        'mw_data': mw_data,
        'targets': pairs,
        'ex_tickers': exchange_data,
        'all_exchanges': all_exchanges(),
        'volumes': volumes(),
        'daily_mined': daily_mined(models()['epic']),
        'high_low_7d': high_low_7d(models()['epic']),
        'high_low_7d_btc': high_low_7d(models()['epic'], '_btc'),
        'filters': filters(),
        'links': Link.objects.all(),
        'other_coins': [coin for coin in all_coins() if not coin.mw_coin]
        }

    return render(request, "home.html", context)


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        template = loader.get_template('pages/' + load_template)
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('pages/error-404.html')
        return HttpResponse(template.render(context, request))

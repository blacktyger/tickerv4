from datetime import timedelta
from time import monotonic

from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.base import View, TemplateView
from rest_framework import viewsets

from .serializers import DataSerializer
from .models import *
from .templatetags.calculations import daily_mined, \
    high_low_7d
from .coins.data import models, volumes
from .globals import pairs
from .templatetags.calculations import halving


class DataViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Epic Cash data.
    """
    queryset = Data.objects.order_by('-updated')[0:2]
    serializer_class = DataSerializer


class IndexView(TemplateView):
    context_object_name = 'home_list'
    template_name = 'home-test.html'
    model = Data

    def charts(self):
        for chart in Chart.objects.filter(name='mw_chart'):
            if chart.coin.mw_coin:
                self.mw_data[chart.coin.symbol].update(
                    {'chart': {'div': chart.div, 'script': chart.script}})

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['filters'] = {
            'epic': {
                'coin': models()['epic'],
                'gecko': models()['epic'].coingecko.order_by('updated').last(),
                'explorer': models()['epic'].explorer.order_by('updated').last(),
                'data': {
                    'all': models()['epic'].data.all(),
                    'usdt': Data.objects.filter(coin=models()['epic'], pair='usdt').order_by('updated').last(),
                    'btc': Data.objects.filter(coin=models()['epic'], pair='btc').order_by('updated').last(),
                    'last': [Data.objects.filter(coin=models()['epic'], pair='usdt').order_by('updated').last(),
                             Data.objects.filter(coin=models()['epic'], pair='btc').order_by('updated').last()]
                    }},
            'bitcoin': {
                'coin': models()['btc'],
                'gecko': models()['btc'].coingecko.latest('updated').data
                },
            'exchanges': {
                'citex': {
                    'details': models()['citex'],
                    'tickers': {
                        'all': models()['citex'].ticker.all(),
                        'usdt': models()['citex'].ticker.filter(pair='usdt'),
                        'btc': models()['citex'].ticker.filter(pair='btc'),
                        'last': [models()['citex'].ticker.filter(pair='usdt').order_by('updated').last(),
                                 models()['citex'].ticker.filter(pair='btc').order_by('updated').last()],
                        }},
                'vitex': {
                    'details': models()['vitex'],
                    'tickers': {
                        'all': models()['vitex'].ticker.all(),
                        'usdt': models()['vitex'].ticker.filter(pair='usdt'),
                        'btc': models()['vitex'].ticker.filter(pair='btc'),
                        'last': [models()['vitex'].ticker.filter(pair='usdt').order_by('updated').last(),
                                 models()['vitex'].ticker.filter(pair='btc').order_by('updated').last()],
                        }}
                },
            'charts': {
                'epic_7d_price': Chart.get.by_name(name='epic_7d_price').latest(),
                'epic_vol_24h': Chart.get.by_name(name='vol_24h').latest(),
                },
            }
        context['ex_tickers'] = {
            ex: {
                target: ex.ticker.filter(pair=target).order_by('updated').last() for target in pairs
                if ex.ticker.filter(pair=target)} for ex in Exchange.objects.all()}
        context['currency'] = Currency.objects.all(),
        context['links'] = Link.objects.all(),
        context['epic'] = Coin.get.by_name('epic-cash'),
        context['other_coins'] = Coin.objects.filter(mw_coin=False),
        context['last_update'] = Data.get.latest().updated,
        context['halving'] = halving(models()['epic']),
        context['mw_data'] = {coin.symbol: CoinGecko.get.by_coin(coin).latest().data
                              for coin in Coin.objects.filter(mw_coin=True)},
        context['volumes'] = volumes(),
        context['daily_mined'] = daily_mined(models()['epic']),
        context['high_low_7d'] = high_low_7d(models()['epic']),
        context['high_low_7d_btc'] = high_low_7d(models()['epic'], '_btc'),
        context['update_data'] = update_data(),

        return context


def index(request):
    start_time = monotonic()

    template = loader.get_template('home.html')

    mw_data = {coin.symbol: CoinGecko.objects.filter(coin=coin).latest('updated').data
               for coin in Coin.objects.filter(mw_coin=True)}

    for chart in Chart.objects.filter(name='mw_chart'):
        if chart.coin.mw_coin:
            mw_data[chart.coin.symbol].update({'chart':
                                                   {'div': chart.div,
                                                    'script': chart.script}})

    exchange_data = {ex: {
        target: ex.ticker.filter(pair=target).order_by('updated').last() for target in pairs
        if ex.ticker.filter(pair=target)} for ex in Exchange.objects.all()}

    def update_data():
        data = {}
        for model in all_models:
            data[str(model).split('.')[2][:-2]] = model.objects.order_by('updated').last().updated
        return data

    filterss = {
        'epic': {
            'coin': models()['epic'],
            'gecko': models()['epic'].coingecko.order_by('updated').last(),
            'explorer': models()['epic'].explorer.order_by('updated').last(),
            'data': {
                'all': models()['epic'].data.all(),
                'usdt': Data.objects.filter(coin=models()['epic'], pair='usdt').order_by('updated').last(),
                'btc': Data.objects.filter(coin=models()['epic'], pair='btc').order_by('updated').last(),
                'last': [Data.objects.filter(coin=models()['epic'], pair='usdt').order_by('updated').last(),
                         Data.objects.filter(coin=models()['epic'], pair='btc').order_by('updated').last()]
                }},
        'bitcoin': {
            'coin': models()['btc'],
            'gecko': models()['btc'].coingecko.latest('updated').data
            },
        'exchanges': {
            'citex': {
                'details': models()['citex'],
                'tickers': {
                    'all': models()['citex'].ticker.all(),
                    'usdt': models()['citex'].ticker.filter(pair='usdt'),
                    'btc': models()['citex'].ticker.filter(pair='btc'),
                    'last': [models()['citex'].ticker.filter(pair='usdt').order_by('updated').last(),
                             models()['citex'].ticker.filter(pair='btc').order_by('updated').last()],
                    }},
            'vitex': {
                'details': models()['vitex'],
                'tickers': {
                    'all': models()['vitex'].ticker.all(),
                    'usdt': models()['vitex'].ticker.filter(pair='usdt'),
                    'btc': models()['vitex'].ticker.filter(pair='btc'),
                    'last': [models()['vitex'].ticker.filter(pair='usdt').order_by('updated').last(),
                             models()['vitex'].ticker.filter(pair='btc').order_by('updated').last()],
                    }}
            },
        'charts': {
            'epic_7d_price': Chart.objects.filter(name='epic_7d_price').order_by('updated').last(),
            'epic_vol_24h': Chart.objects.filter(name='vol_24h').order_by('updated').last(),
            },
        }

    context = {
        'last_update': Data.objects.order_by('updated').last().updated,
        'update_data': update_data(),
        'coins_list': Coin.objects.all(),
        'currency': Currency.objects.all(),
        'halving': halving(models()['epic']),
        'mw_data': mw_data,
        'targets': pairs,
        'ex_tickers': exchange_data,
        'volumes': volumes(),
        'daily_mined': daily_mined(models()['epic']),
        'high_low_7d': high_low_7d(models()['epic']),
        'high_low_7d_btc': high_low_7d(models()['epic'], '_btc'),
        'filters': filterss,
        'links': Link.objects.all(),
        'other_coins': Coin.objects.filter(mw_coin=False)
        }
    end_time = monotonic()
    print(f"{timedelta(seconds=(end_time - start_time)).total_seconds()} seconds")
    return HttpResponse(template.render(context, request))


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

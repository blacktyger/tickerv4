import json
from time import sleep, monotonic
from datetime import timedelta

import requests
from django.utils import timezone
from pycoingecko import CoinGeckoAPI
import copy
from app.globals import pairs
from app.tools import t_s, d, spread, avg, get_gecko, get_ticker, \
    fields, updater, api, get_flag, btc_to_usd, usd_to_btc
from app.models import Coin, Exchange, Data, Ticker, CoinGecko, \
    Chart, Explorer, Pool, Link, Currency


API_KEY = '46da25a4b62cbb6e531bfc39'

PAIRS = pairs
cg = CoinGeckoAPI()

EXCHANGES = ['CITEX', 'ViteX']

POOLS = ['icemining', '51pool']

LINKS = [
    ['Telegram', 'https://t.me/EpicCash', 'fa fa-telegram', 'social'],
    ['Medium', 'https://medium.com/epic-cash', 'fa fa-medium', 'social'],
    ['Twitter', 'https://twitter.com/EpicCashTech', 'fa fa-twitter', 'social'],
    ['Reddit', 'https://www.reddit.com/r/epiccash/', 'fa fa-reddit', 'social'],
    ['Instagram', 'https://www.instagram.com/explore/tags/epiccash/', 'fa fa-instagram', 'social'],
    ['Discord', 'https://discordapp.com/invite/ZjnC6bh', 'fab fa-discord', 'social'],
    ['Explorer', 'https://explorer.epic.tech/', 'fa fa-table', 'tech'],
    ['White Paper', 'https://epic.tech/whitepaper/', 'fa fa-file', 'tech'],
    ['GitLab', 'https://gitlab.com/epiccash', 'fa fa-gitlab', 'tech'],
    ['Guides', 'https://epic.tech/guidestutorials/', 'fa fa-question-circle', 'tech'],
    ]

COINS = {
    'mw_coins': [
        ('epic-cash', 'EPIC'),
        ('grin', 'GRIN'),
        ('beam', 'BEAM'),
        ('mimblewimblecoin', 'MWC'),
        ('grimm', 'XGM'),
        ('bitgrin', 'XBG'),
        ],
    'other': [
        ('bitcoin', 'BTC'),
        ('ethereum', 'ETH'),
        ('monero', 'XMR'),
        ]
    }

CURRS = {
    'EU': 'EUR',
    'GB': 'GBP',
    'JP': 'JPY',
    'CN': 'CNY',
    'PL': 'PLN',
    'RU': 'RUB',
    'PH': 'PHP',
    'VE': 'VES',
    }


def links():
    for link in LINKS:
        Link.objects.get_or_create(name=link[0], link=link[1], icon=link[2], category=link[3])
    return f"{len(Link.objects.all())} Links saved to models"


def coins():
    for type_, coins in COINS.items():
        for coin in coins:
            if type_ == "mw_coins":
                Coin.objects.get_or_create(name=coin[0], symbol=coin[1], mw_coin=True)
            else:
                Coin.objects.get_or_create(name=coin[0], symbol=coin[1], mw_coin=False)
    return f"{len(Coin.objects.all())} coins saved to models"


def exchanges():
    for exchange in EXCHANGES:
        Exchange.objects.get_or_create(name=exchange)
    return f"{len(Exchange.objects.all())} exchanges saved to models"


def pools():
    for pool in POOLS:
        Pool.objects.get_or_create(name=pool, coin=models()['epic'])
    return f"{len(Pool.objects.all())} pools saved to models"


def all_coins():
    return [coin for coin in Coin.objects.all()]


def all_exchanges():
    return [exchange for exchange in Exchange.objects.all()]


def models():
    return {
        'citex': Exchange.objects.get(name='CITEX'),
        'vitex': Exchange.objects.get(name='ViteX'),
        'epic': Coin.objects.get(symbol='EPIC'),
        'btc': Coin.objects.get(symbol='BTC'),
        'icemining': Pool.objects.get(name='icemining')
        }


def filters():
    return {
        'epic': {
            'coin': models()['epic'],
            'gecko': models()['epic'].coingecko.last(),
            'explorer': models()['epic'].explorer.last(),
            'data': {
                'all': models()['epic'].data.all(),
                'usdt': Data.objects.filter(coin=models()['epic'], pair='usdt'),
                'btc': Data.objects.filter(coin=models()['epic'], pair='btc'),
                'last': [Data.objects.filter(coin=models()['epic'], pair='usdt').last(),
                         Data.objects.filter(coin=models()['epic'], pair='btc').last()]
                }},
        'bitcoin': {
            'coin': models()['btc'],
            'gecko': models()['btc'].coingecko.last().data
            },
        'exchanges': {
            'citex': {
                'details': models()['citex'],
                'tickers': {
                    'all': models()['citex'].ticker.all(),
                    'usdt': models()['citex'].ticker.filter(pair='usdt'),
                    'btc': models()['citex'].ticker.filter(pair='btc'),
                    'last': [models()['citex'].ticker.filter(pair='usdt').last(),
                             models()['citex'].ticker.filter(pair='btc').last()],
                    }},
            'vitex': {
                'details': models()['vitex'],
                'tickers': {
                    'all': models()['vitex'].ticker.all(),
                    'usdt': models()['vitex'].ticker.filter(pair='usdt'),
                    'btc': models()['vitex'].ticker.filter(pair='btc'),
                    'last': [models()['vitex'].ticker.filter(pair='usdt').last(),
                             models()['vitex'].ticker.filter(pair='btc').last()],
                    }}
            },
        'charts': {
            # 'btc': [models()['btc'].chart.get().div, models()['btc'].chart.get().script],
            'epic_7d_price': Chart.objects.get(name='epic_7d_price'),
            'epic_vol_24h': Chart.objects.get(name='vol_24h'),
            },
        }


def exchange_details(exchange, save=False):
    start_time = monotonic()
    data = {key: value for key, value in
            cg.get_exchanges_by_id(exchange.name).items() if key != 'tickers'}
    updater(exchange, data)
    end_time = monotonic()
    return f"Exchange Details saved in db {timedelta(seconds=end_time - start_time)}"


def currency_data(save=False):
    start_time = monotonic()

    def get_rates():
        url = 'https://v6.exchangerate-api.com/v6/'
        rates = api(url, API_KEY + '/latest/USD')
        return {x: y for x, y in rates['conversion_rates'].items()}

    data = {}
    source = get_rates()
    for currency, price in source.items():
        for key, value in CURRS.items():
            if currency == value:
                new, created = Currency.objects.get_or_create(symbol=value)
                new.flag = get_flag(key)
                new.price = price
                new.country = key
                new.save()
    end_time = monotonic()
    return f"Currency data saved in db {timedelta(seconds=end_time - start_time)}"


def coingecko_data(save=False):
    start_time = monotonic()
    for coin in all_coins():
        # print(f"{coin}...")
        source = copy.deepcopy(cg.get_coin_by_id(coin.name))
        data = {
            'name': source['name'].capitalize(),
            'symbol': source['symbol'].upper(),
            'img': source['image']['large'],
            'market_cap': d(source['market_data']['market_cap']['usd'], 2),
            'volume': d(source['market_data']['total_volume']['usd'], 2),
            'price': d(cg.get_price(coin.name, 'usd')[coin.name]['usd'], 4),
            'price_7d': cg.get_coin_market_chart_by_id(coin.name, 'usd', 7)['prices'],
            'change_24h': d(source['market_data']['price_change_percentage_24h'], 2),
            'change_7d': d(source['market_data']['price_change_percentage_7d'], 2),
            'ath': {
                'usdt': {
                    'price': source['market_data']['ath']['usd'],
                    'date': source['market_data']['ath_date']['usd'],
                    'change': source['market_data']['ath_change_percentage']['usd']
                    },
                'btc': {
                    'price': source['market_data']['ath']['btc'],
                    'date': source['market_data']['ath_date']['btc'],
                    'change': source['market_data']['ath_change_percentage']['btc']
                    }}
            }

        if save:
            CoinGecko.objects.create(coin=coin, data=data)
        else:
            if CoinGecko.objects.filter(coin=coin).last():
                x = CoinGecko.objects.filter(coin=coin).last()
                x.updated = timezone.now()
                x.data = data
                x.save()
            else:
                CoinGecko.objects.create(coin=coin, data=data)

    end_time = monotonic()
    return f"CoinGecko data saved in db {timedelta(seconds=end_time - start_time)}"


def citex_data(save=False):
    start_time = monotonic()

    def citex_api(que, sym='epic_usdt', si='', ty='', breaks=False):
        """ Create proper urls for API end points """
        start_url = "https://api.citex.co.kr/v1/"
        query = que + '?'
        symbol = 'symbol=' + sym
        size = '&size=' + si
        typ = '&type=' + ty
        url = start_url + query + symbol + size + typ
        if breaks:
            sleep(1.3)
        # print(f"{url}...")
        return json.loads(requests.get(url).content)

    data = {target: {} for target in PAIRS}

    for coin in all_coins()[:1]:
        source = copy.deepcopy(citex_api('alltickers')['ticker'])
        for target in PAIRS:
            vol = [d(x[::5][1]) for x in citex_api('candles', sym='epic_' + target, si="24", ty="60", breaks=True)]
            vol = sum(vol)
            for tick in source:
                if tick['symbol'] == coin.symbol.lower() + '_' + target:
                    data[target].update(tick)
                    sleep(1.3)

            update = {
                'id': int(len(Ticker.objects.all())) + 1,
                'updated': timezone.now(),
                'coin': coin,
                'exchange': models()['citex'],
                'pair': target,
                'trading_url': 'https://trade.citex.me/trade/' + coin.symbol + '_' + target.upper(),
                'last_price': d(data[target]['last']),
                'bid': d(data[target]['buy']),
                'ask': d(data[target]['sell']),
                'spread': spread(data[target]['sell'], data[target]['buy']),
                'high': d(data[target]['high']),
                'low': d(data[target]['low']),
                'last_trade': t_s(citex_api('trades', sym='epic_' + target, si="1", breaks=True)[0]['timestamp']),
                'volume': d(vol),
                'orders': citex_api('depth', sym='epic_' + target, si="10", breaks=True),
                'candles': {
                    'candles': citex_api('candles', sym='epic_' + target, si="1", ty="60", breaks=True),
                    'c7x1440': [[t_s(x[::5][0]), float(x[::5][1])] for x in
                                citex_api('candles', sym='epic_' + "usdt", si="7", ty="1440", breaks=True)],
                    },
                'trades': citex_api('trades', sym='epic_' + target, si="10", breaks=True),
                }
            sleep(1.5)
            if save:
                Ticker.objects.create(**update)
            else:
                x = Ticker.objects.filter(
                    coin=coin, pair=target, exchange=models()['citex']).last()
                updater(x, update)

    end_time = monotonic()
    return f"Citex Data saved in db {timedelta(seconds=end_time - start_time)}"


def vitex_data(save=False):
    start_time = monotonic()
    queries = {
        'depth': 'depth?symbol=',
        'orderbook': 'ticker/bookTicker?symbol=',
        'ticker': 'ticker/24hr?symbols=',
        'market': 'market?symbol=',
        'trades': 'trades?symbol=',
        'candles': 'klines?symbol=',
        }
    symbol = 'EPIC-001_BTC-000'
    coin = models()['epic']
    target = 'btc'

    def vitex_api(query, breaks=False, extra='&interval=hour&limit=20'):
        start_url = "https://api.vitex.net/api/v2/"
        if query == "klines?symbol=":
            url = start_url + query + symbol + extra
        else:
            url = start_url + query + symbol
        # print(f"{url}...")
        if breaks:
            sleep(1.5)
        return json.loads(requests.get(url).content)

    data = {query: vitex_api(queries[query]) for query in queries}
    update = {
        'id': int(len(Ticker.objects.all())) + 1,
        'updated': timezone.now(),
        'coin': coin,
        'exchange': models()['vitex'],
        'pair': target,
        'trading_url': 'https://x.vite.net/trade?symbol=' + symbol,
        'last_price': d(data['market']['data']['lastPrice']),
        'bid': d(data['market']['data']['bidPrice']),
        'ask': d(data['market']['data']['askPrice']),
        'spread': spread(data['market']['data']['askPrice'], data['market']['data']['bidPrice']),
        'high': d(data['market']['data']['highPrice']),
        'low': d(data['market']['data']['lowPrice']),
        'last_trade': t_s(data['trades']['data'][0]['timestamp']),
        'volume': d(data['market']['data']['volume']),
        'orders': data['depth']['data'],
        'candles': data['candles']['data'],
        'trades': data['trades']['data']
        }

    if save:
        Ticker.objects.create(**update)
    else:
        x = Ticker.objects.filter(
            coin=models()['epic'], pair=target, exchange=models()['vitex']).last()
        updater(x, update)

    end_time = monotonic()
    return f"ViteX Data saved in db {timedelta(seconds=end_time - start_time)}"


def pool_data():
    parts = {
        'icemining': {
            'url': 'https://icemining.ca/api/',
            'params': ['blocks/epic/']},
        '51pool': {
            'url': 'https://51pool.online/api/',
            'params': ['blocks/'],
            }
        }

    for pool in POOLS:
        pool_to_update, created = Pool.objects.get_or_create(
            name=pool, coin=models()['epic'])
        pool_to_update.updated = timezone.now()
        pool_to_update.blocks = api(parts[pool]['url'], parts[pool]['params'][0])[0:50]
        pool_to_update.save()

    return f"Pool data saved to db!"


def explorer_data(save=False):
    parts = {
        'ex_url': 'https://explorer.epic.tech/api?q=',
        'ex_params': [
            'circulating', 'getblockcount', 'getdifficulty-randomx',
            'getdifficulty-progpow', 'getdifficulty-cuckoo', 'reward',
            'average-blocktime', 'getblocktime&height='
            ],
        'ice_url': 'https://icemining.ca/api/',
        'ice_params': ['blocks/epic/']
        }

    data = {
        'coin': models()['epic'],
        'updated': timezone.now(),
        'last_block': t_s(api(parts['ex_url'], parts['ex_params'][7]
                              + str(api(parts['ex_url'], parts['ex_params'][1])))),
        'circulating': api(parts['ex_url'], parts['ex_params'][0]),
        'height': api(parts['ex_url'], parts['ex_params'][1]),
        'reward': api(parts['ex_url'], parts['ex_params'][5]),
        'average_blocktime': api(parts['ex_url'], parts['ex_params'][6]),
        'target_diff': {
            'progpow': [block for block in models()['icemining'].blocks if block['algo'] == 'progpow'][0]['diff'],
            'randomx': [block for block in models()['icemining'].blocks if block['algo'] == 'randomx'][0]['diff'],
            # 'cuckoo': [block for block in models()['icemining'].blocks if block['algo'] == 'cuckoo'][0]['diff']
            },
        'total_diff': {
            'progpow': api(parts['ex_url'], parts['ex_params'][3]),
            'randomx': api(parts['ex_url'], parts['ex_params'][4]),
            'cuckoo': api(parts['ex_url'], parts['ex_params'][5]),
            }
        }

    if save:
        Explorer.objects.create(**data)
    else:
        x = Explorer.objects.filter(coin=models()['epic']).last()
        updater(x, data)

    end_time = monotonic()
    return f"Explorer data saved to db!"


def epic_data(save=False):
    start_time = monotonic()

    coin = models()['epic']
    tickers = {target:
                   {ex: Ticker.objects.filter(
                       coin=coin, exchange=ex,
                       pair=target).last() for ex in EXCHANGES
                    if Ticker.objects.filter(
                       coin=coin, exchange=ex, pair=target)}
               for target in PAIRS}

    def avg_price(coin, currency):
        coin = models()['epic']
        source = {target:
                      [float(Ticker.objects.filter(
                          coin=coin, exchange=ex,
                          pair=target).last().last_price) for ex in EXCHANGES
                       if Ticker.objects.filter(
                          coin=coin, exchange=ex, pair=target)]
                  for target in PAIRS}
        prices = []
        for target in PAIRS:
            if target == currency:
                prices.append(avg(source[target]))
            else:
                if currency == 'usdt':
                    prices.append(btc_to_usd(avg(source[target])))
                elif currency == "btc":
                    prices.append(usd_to_btc(avg(source[target])))
        return avg(prices)

    for target in PAIRS:
        data = {
            'coin': models()['epic'],
            'pair': target,
            'updated': timezone.now(),
            'avg_price': d(avg_price(models()['epic'], target)),
            'vol_24h': sum([d(x.volume) for x in tickers[target].values()]),
            'percentage_change_24h': get_gecko(models()['epic']).data['change_24h'],
            'percentage_change_7d': get_gecko(models()['epic']).data['change_7d'],
            'market_cap': d(
                filters()['epic']['explorer'].circulating) * avg([x.last_price for x in tickers[target].values()]),
            'ath': d(get_gecko(models()['epic']).data['ath'][target]['price']),
            'ath_date': get_gecko(models()['epic']).data['ath'][target]['date'],
            'ath_change': d(get_gecko(models()['epic']).data['ath'][target]['change'], 2),
            'block_value': d(filters()['epic']['explorer'].reward) *
                           d(avg_price(models()['epic'], target)),
            }
        if save:
            Data.objects.create(**data)
        else:
            x = Data.objects.filter(coin=models()['epic'], pair=target).last()
            updater(x, data)

    end_time = monotonic()
    return f"Epic-Cash Data saved in db {timedelta(seconds=end_time - start_time)}"


def volumes():
    vols = {
        'citex_btc': d(filters()['exchanges']['citex']['tickers']['btc'].last().volume),
        'vitex_btc': d(filters()['exchanges']['vitex']['tickers']['btc'].last().volume),
        'citex_usdt': d(filters()['exchanges']['citex']['tickers']['usdt'].last().volume)
        }

    total = vols['citex_btc'] + vols['citex_usdt'] + vols['vitex_btc']
    usdt = vols['citex_usdt']
    btc = vols["vitex_btc"] + vols['citex_btc']
    citex = vols['citex_btc'] + vols['citex_usdt']
    vitex = vols["vitex_btc"]

    btc_vs_total = d(btc / total * 100, 0)
    usdt_vs_total = d(usdt / total * 100, 0)
    citex_vs_total = d(citex / total * 100, 0)
    vitex_vs_total = d(vitex / total * 100, 0)

    return {
        'total': {
            'all': total,
            'usdt': usdt,
            'btc': btc,
            },
        'citex': {
            'total': citex,
            'usdt': vols['citex_usdt'],
            'btc': vols['citex_btc'],
            },
        'vitex': {
            'total': vitex,
            'btc': vols['vitex_btc'],
            },
        'percent': {
            'btc': [btc, btc_vs_total],
            'usdt': [usdt, usdt_vs_total],
            'CITEX': [citex, citex_vs_total],
            'ViteX': [vitex, vitex_vs_total]
            }}

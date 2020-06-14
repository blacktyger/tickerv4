from datetime import timedelta
from time import monotonic

from .models import *
from app.templatetags.calculations import daily_mined, \
    high_low_7d
from app.coins.data import *
from app.coins.charts import *
from background_task import background
from app.coins.charts import main_charts, mw_charts
from .globals import pairs


@background(schedule=1)
def update_10():
    start_time = monotonic()
    for exchange in all_exchanges():
        exchange_details(exchange)
    coingecko_data()
    currency_data()
    end_time = monotonic()
    return print(f'[EXCHANGE | COINGECKO | CURRENCY] {timezone.now()} | {timedelta(seconds=end_time - start_time)}')


@background(schedule=1)
def update_2():
    start_time = monotonic()
    citex_data()
    vitex_data()
    main_charts()
    mw_charts()
    end_time = monotonic()
    return print(f'[CITEX | VITEX] {timezone.now()} | {timedelta(seconds=end_time - start_time)}')


@background(schedule=1)
def update_1():
    start_time = monotonic()
    pool_data()
    explorer_data()
    epic_data()
    end_time = monotonic()
    return print(f'[POOL | EXPLORER | EPIC] {timezone.now()} | {timedelta(seconds=end_time - start_time)}')


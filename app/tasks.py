from datetime import timedelta
from time import monotonic

from .models import *
from .templatetags.calculations import daily_mined, \
    high_low_7d
from .coins.data import *
from background_task import background
from .coins.charts import main_charts, mw_charts
from .globals import pairs


def update(tasks, save=False):
    start_time = monotonic()
    print(f"[{timezone.now().strftime('%H:%M:%S')}] START >> {[str(task).split(' ')[1] for task in tasks]}")
    for task in list(tasks):
        task(save=save)
        # print(f"{str(task).split(' ')[1]}")

    end_time = monotonic()
    return print(f"[{timezone.now().strftime('%H:%M:%S')}] END >> TIME: {timedelta(seconds=end_time - start_time).total_seconds()} SECONDS")


@background(schedule=120)
def up_data1():
    tasks = [coingecko_data, explorer_data, currency_data]
    update(tasks)
    return f'OK'


@background(schedule=300)
def up_exchanges():
    tasks = [citex_data, vitex_data]
    update(tasks)
    return f'OK'


@background(schedule=60)
def up_data2():
    tasks = [epic_data, mw_charts, main_charts]
    update(tasks)
    return f'OK'


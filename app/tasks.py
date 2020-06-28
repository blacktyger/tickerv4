from background_task.models import Task
from .models import *
from .coins.data import *
from background_task import background
from .coins.charts import main_charts, mw_charts


def clear_db_task(name):
    db_record = Task.objects.filter(verbose_name=name)
    if db_record.exists():
        db_record.delete()
        return print(f"{name} deleted")


def update(tasks):
    start_time = monotonic()
    print(f"[{timezone.now().strftime('%H:%M:%S')}] {[str(task).split(' ')[1] for task in tasks]} -- START")
    for task in list(tasks):
        # try:
        task()
        print(f"{str(task).split(' ')[1]}")
        # except:
        # print(f"GOOOOOOOOOOOOOOOOOOOOOWNOOOOOOOOOO")
        # continue
    end_time = monotonic()
    return print(f"[{timezone.now().strftime('%H:%M:%S')}] {[str(task).split(' ')[1] for task in tasks]} -- END IN TIME: {timedelta(seconds=end_time - start_time).total_seconds()} SECONDS")


@background(schedule=300)
def up_data1():
    tasks = [pool_data, coingecko_data, explorer_data]
    update(tasks)
    return f'OK'


@background(schedule=300)
def up_exchanges():
    tasks = [citex_data, vitex_data]
    update(tasks)
    return f'OK'


@background(schedule=300)
def up_data2():
    tasks = [epic_data, mw_charts, main_charts]
    update(tasks)
    return f'OK'


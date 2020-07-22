from .models import Travel


def calc_fuel():
    for fuel in Travel.objects.all():
        return float(fuel.price)


def calc_cons():
    for cons in Travel.objects.all():
        return float(cons.amount)


def fuel_cost(distance):
    fuel_price = calc_fuel()
    fuel_consumption = calc_cons()
    cost = distance / 100 * fuel_consumption * fuel_price
    return cost


def hours(time):
    min, sec = divmod(time, 60)
    hour, min = divmod(min, 60)
    return "%d:%02d" % (hour, min)


def if_last(job_list):
    if len(job_list) >= 1:
        job_list = job_list[-1]
    else:
        job_list
    return job_list

import datetime
import googlemaps as gm
import requests
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Travel
from .tools import *
from .forms import TravelForm

gmaps = gm.Client(key='AIzaSyA3kk4GM2S2azg_5-J7YCKtX3ApmVePZ9U')


def distance(request):
    user_travels = Travel.objects.all()
    instance = user_travels.last()
    form = TravelForm(request.POST or None, instance=instance)

    if request.method == "POST":
        if form.is_valid():
            try:
                data = gmaps.directions(
                    form.cleaned_data['origin'],
                    form.cleaned_data['destination'])[0]['legs'][0]
                new_travel = Travel(
                    amount=form.cleaned_data['amount'],
                    price=form.cleaned_data['price'],
                    destination=data['end_address'],
                    origin=data['start_address'],
                    # destination=form.cleaned_data['destination'],
                    # origin=form.cleaned_data['origin'],
                    date=datetime.datetime.now(),
                    distance=round(data['distance']['value'] / 1000 * 0.62, 2),
                    time=hours(data['duration']['value']),
                    cost=round(fuel_cost(round(data['distance']['value'] / 1000, 2)), 2),
                    dest_link='https://www.google.com/maps/search/' + form.cleaned_data['destination'],
                    origin_link='https://www.google.com/maps/search/' + form.cleaned_data['origin'],
                    destination_full=data['end_address'],
                    origin_full=data['start_address'],
                    )
                form.save()
                new_travel.save()

                return HttpResponseRedirect(reverse('calc'))
            except gm.exceptions.ApiError as error:
                messages.warning(request, f'Address not found!')

    context = {
        'travels': user_travels,
        'last_job': user_travels.last(),
        'job_form': form,
        }

    return render(request, 'calc.html', context)


# block_target_time = 60
# price = 0.20
# rig_hashrate = 14_000
#
#
# def block_reward():
#     reward = 8
#     tax = 0.6216
#     return reward - tax
#
#
# def blocks_per_day():
#     block_time = 69
#     return 86400 / block_time
#
#
# def network_hashrate():
#     """
#     current_diff = last_block_total_diff - previous_block_total_diff
#     """
#     current_diff = 651_859_373
#     return current_diff / block_target_time
#
#
# def rig_cost(kwh_cost, wattage, time=24):
#     """
#     calculate rig cost based on :kwh_cost (cents), :wattage in given :time (hours)
#     """
#     return (kwh_cost / 1000) * wattage * time
#
#
# def rig_profit(rig_hashrate=rig_hashrate, price=price):
#     """
#     calculate rig profit based on :rig_hashrate and :price
#     (block_reward * blocks_per_day) / network_hashrate * rig_hashrate * price
#     """
#     yield_ = (block_reward() * blocks_per_day()) / network_hashrate() * rig_hashrate
#     profit = yield_ * price
#     return f"{round(yield_, 2)} coins, ${round(profit, 2)}"
#
#
# def solo_block_time(rig_hashrate=rig_hashrate):
#     """
#     Caclulate time needed to mine block solo with given :rig_hashrate
#     (network_hashrate() * block_target_time / (rig_hashrate * 1_000_000)) / 86400
#     or
#     network_hashrate() / rig_hashrate * block_target_time
#     """
#     #     one = (network_hashrate() * block_target_time / (rig_hashrate * 1_000_000)) / 86400
#     return round(((network_hashrate() / rig_hashrate) * block_target_time) / (60 * 60), 2)

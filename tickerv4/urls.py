# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from background_task.models import Task
from time import sleep

from django.contrib import admin
from django.urls import path, include  # add this
from app.tasks import up_data1, up_data2, up_exchanges

urlpatterns = [
    # path('api/', include('epic_api.urls')),
    path('admin/', admin.site.urls),
    # path("", include("authentication.urls")),  # add this
    path("", include("app.urls"))  # add this
    ]

if not Task.objects.filter(verbose_name="up_data1").exists():
    up_data1(repeat=120, verbose_name="up_data1")

if not Task.objects.filter(verbose_name="up_data2").exists():
    up_data2(repeat=60, verbose_name="up_data2")

if not Task.objects.filter(verbose_name="up_exchanges").exists():
    up_exchanges(repeat=300, verbose_name="up_exchanges")
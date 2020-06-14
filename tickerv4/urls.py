# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from app.tasks import update_1, update_2, update_10

urlpatterns = [
    # path('api/', include('epic_api.urls')),
    path('admin/', admin.site.urls),
    # path("", include("authentication.urls")),  # add this
    path("", include("app.urls"))  # add this
]

update_1(repeat=120)
update_2(repeat=240)
update_10(repeat=600)
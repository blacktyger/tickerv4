import time

from rest_framework import serializers

from .models import *


class DataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Data
        exclude = ['id', 'explorer', 'coin', 'to_save', 'ath', 'ath_date']


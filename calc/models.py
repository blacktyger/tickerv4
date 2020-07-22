from django_extensions.db.fields.json import JSONField
from app.models import Data, Currency, Explorer, Ticker
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Travel(models.Model):
    destination = models.CharField(max_length=50, blank=False)
    origin = models.CharField(max_length=50, blank=False)
    amount = models.FloatField(default='9', blank=False, null=False)
    price = models.FloatField(default='1.3', blank=False, null=False)

    date = models.DateTimeField(default=timezone.now)
    distance = models.CharField(max_length=20, blank=True)
    time = models.CharField(max_length=15, blank=True)
    cost = models.CharField(max_length=15, blank=True)
    dest_link = models.URLField(blank=True)
    origin_link = models.URLField(blank=True)
    destination_full = models.CharField(max_length=50, blank=True)
    origin_full = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"({self.destination} from {self.origin} "
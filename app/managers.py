from django.db import models

"""
Custom QuerySets and Managers for advanced  queries in database.
"""


class DataQuerySet(models.QuerySet):
    def by_coin(self, coin):
        return self.filter(coin=coin)

    def latest(self):
        return self.order_by('updated').last()

    def by_pair(self, coin):
        return self.filter(pair=coin)

    def by_name(self, name):
        return self.filter(name=name)


class TickerQuerySet(models.QuerySet):
    def latest(self):
        return self.order_by('updated').last()

    def by_ex(self, exchange):
        return self.filter(exchange=exchange)

    def by_pair(self, coin):
        return self.filter(pair=coin)

    def by_coin(self, coin):
        return self.filter(coin=coin)

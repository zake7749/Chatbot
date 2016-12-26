# coding=utf-8

"""
This class is for building and return a task handler
based on the task's domain.
"""

from .medicine import medicine
from .other.weather import Weather
from .other.stock import Stock
from .purchase import purchase
from .entertainment import entertainment
from .hotel import hotel
class Switch(object):

    def __init__(self, console):
        self.console = console

    def get_handler(self, domain):

        handler = None

        if domain == "病症":
            handler = medicine.MedicalListener(self.console)
        elif domain=="天氣":
            handler = Weather(self.console)

        elif domain=="股票":
            handler = Stock(self.console)

        #elif domain=="購買":
        #    handler = purchase.PurchaseOperator(self.console)
        #elif domain=="吃喝玩樂":
        #    handler = entertainment.entertainment(self.console)
        #elif domain=="住宿":
        #    handler = hotel.HotelListener(self.console)
        else:
            pass
        return handler

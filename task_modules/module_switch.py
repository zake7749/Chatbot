"""
This class is for building and return a task handler
based on the task's domain.
"""
from .medicine import medicine
from .other.weather import Weather
from .other.stock import Stock
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
        else:
            pass    
        """

        """
        return handler

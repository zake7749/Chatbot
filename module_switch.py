"""
This class is for building and return a task handler
based on the task's domain.
"""
import task_modules.medicine.medicine as medicine

class Switch(object):

    def __init__(self, console):
        self.console = console

    def get_handler(self, domain):

        handler = None

        if domain == "病症":
            handler = medicine.MedicalListener(self.console)
        else:
            pass
        """

        """
        return handler

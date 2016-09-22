class Task(object):

    def __init__(self, console):
        this.console = console

    def get_response(self,user_input, domain):
        raise NotImplementedError

    def get_query(self):
        raise NotImplementedError

    def has_query(self):
        raise NotImplementedError

    def restore(self, memory):
        raise NotImplementedError

    def get_suggest(self):
        raise NotImplementedError

# -*- coding: utf-8 -*-

import console

def main():
    chatbot = Chatbot()
    chatbot.waiting_loop()

class Chatbot(object):

    def __init__(self, name="NCKU"):
        self.name = name      # The name of chatbot.
        self.last_res = None  # The last matching result.
        self.last_path = None # The last traveling path.
        self.console = console.Console()

    def waiting_loop(self):

        while True:
            speech = input("Hi, I'm " + self.name + '\n')
            self.last_res,self.last_path = self.console.rule_match(speech)
            domain = self.get_baserule()
            self.judge(domain)

    def get_baserule(self):

        """
        Extract the root rule in result.
        """
        if self.last_path == "":
            return self.last_res[1]
        else:
            return(self.last_path.split('>')[0])

    def judge(self, domain):

        print("I know you are talking about '%s', but I don't know how to response." % domain)

if __name__ == '__main__':
    main()

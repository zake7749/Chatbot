# -*- coding: utf-8 -*-

import console
import doctor.diagnose

def main():
    chatbot = Chatbot()
    chatbot.waiting_loop()

class Chatbot(object):

    def __init__(self, name="NCKU"):
        self.name = name      # The name of chatbot.
        self.last_speech = "" # The last user's input
        self.last_res = None  # The last matching result.
        self.last_path = None # The last traveling path.
        self.console = console.Console()

    def waiting_loop(self):

        while True:
            speech = input("Hi, I'm " + self.name + '\n')

            self.last_speech = speech
            self.last_res,self.last_path = self.console.rule_match(speech, best_only=True)

            response = self.console.get_response()

            domain = self.get_baserule()
            self.judge(domain)

    def get_base_domain(self):

        """
        Extract the root rule in result.
        """
        if self.last_path == "":
            return self.last_res[1]
        else:
            return(self.last_path.split('>')[0])

    def judge(self, domain):

        if domain == "病症":
            print("進入醫生模組")
        else:
            print("I know you are talking about '%s', but I don't know how to response." % domain)

if __name__ == '__main__':
    main()

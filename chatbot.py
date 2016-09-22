# -*- coding: utf-8 -*-

import console
import module_switch

def main():
    chatbot = Chatbot()
    chatbot.waiting_loop()

class Chatbot(object):

    def __init__(self, name="NCKU"):
        self.name = name             # The name of chatbot.

        self.speech = ''             # The lastest user's input
        self.speech_domain = ''      # The domain of speech.
        self.speech_matchee = ''     # The matchee term of speech.
        self.speech_path = None      # The classification tree traveling path of speech.
        self.assigneer = None         # The module will handle user's intend.

        self.domain_similarity = 0.0 # The similarity between domain and speech.

        self.console = console.Console(model_path="model/ch-corpus-3sg.bin")

    def waiting_loop(self):

        while True:

            speech = input("Hi, I'm " + self.name + '\n')
            res = self.listen(speech)
            print(res)

    def listen(self, sentence):

        self.rule_match(sentence) # to find the most similar domain with speech.
        handler  = self.module_switch()

        try:
            mem,response = handler.get_response(self.speech, self.speech_domain)
        except AttributeError:
            response = self.get_response()

        if response is None:
            return self.get_response()
        else:
            return response

    def rule_match(self, speech):

        """
        Get the rule has best similarity with user's input,
        and set domain,path,similarity and assigner based on that rule.
        """

        res,self.last_path = self.console.rule_match(speech, best_only=True)
        self.speech = speech
        self.domain_similarity,self.speech_domain,self.speech_matchee = res
        self._set_assigner() # set a module to handle this task.

    def get_response(self):
        """
        Generate a response to user's speech.
        Please note that this response is pre-defined in the json file,
        not the result return by sub_module.
        """
        response = self.console.get_response(self.speech_domain)
        if response is None:
            return "I know you are talking about '%s', but I don't know how to give a response." % self.speech_domain
        else:
            return response

    def _set_assigner(self):

        """
        Extract the root rule in result.
        """
        if self.last_path == "":
            self.assigner = self.speech_domain
        else:
            self.assigner = self.last_path.split('>')[0]

    def module_switch(self):

        switch  = module_switch.Switch(self.console)
        handler = switch.get_handler(self.assigner)

        """
        if in_task:
            #TODO with json format.
            handler.restore(self.speech, memory=None)

        keep,response = handler.get_response(self.speech, self.speech_domain)
        if keep is not None:
            #TODO Restore the history string and user's id on SQL Server.
            pass

        if handler.has_query():
            query_str = handler.get_query()
            # TODO
            # send back the query string to the frontend.
            # Notice that the parsing format of query strings is undefined.
        """

        return handler

if __name__ == '__main__':
    main()

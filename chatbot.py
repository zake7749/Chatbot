# -*- coding: utf-8 -*-

import console
import task_modules.module_switch as module_switch

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

        self.root_domain = None      # The root domain of user's input.
        self.domain_similarity = 0.0 # The similarity between domain and speech.

        self.extract_attr_log = open('log/extract_arrt.log','w',encoding='utf-8')
        self.console = console.Console(model_path="model/ch-corpus-3sg.bin")

    def waiting_loop(self):

        print("你好，我是 " + self.name)
        while True:

            speech = input()
            res = self.listen(speech)
            print(res[0])

    def listen(self, sentence, target=None):

        """
        Listen user's input and send back a response.

        Args:
            - sentence: User's input from frontend.
            - target  : Optional. It is to define the user's input is in form of
            a sentence or a given answer by pressing the bubble buttom.
            If it is come from a button's text, target is the attribute name our
            module want to confirm.

        Return:
            - response : Based on the result of modules or a default answer.
            - status   : It would be the module's current status if the user has
                         been sent into any module and had not left it.
            - target   : Refer to get_query() in task_modules/task.py
            - candiates: Refer to get_query() in task_modules/task.py
        """
        status   = None
        response = None

        self.rule_match(sentence) # find the most similar domain with speech.
        handler = self.get_task_handler()

        try:
            status,response = handler.get_response(self.speech, self.speech_domain, target)
        except AttributeError:
            # It will happen when we call a module which have not implemented.
            # Ref task_modules/module_switch.py and module_switch/task.py
            print("Handler of '%s' have not implemented" % self.root_domain)

        if response is None:
            response = self.get_response()

        if status is None:
            # One pass talking, this sentence does not belong to any task.
            return [response,None,None,None]
        else:
            target,candiates = handler.get_query()
            handler.debug(self.extract_attr_log)
            return [response,status,target,candiates]

    def rule_match(self, speech):

        """
        Set domain,path,similarity,root_domain based on the rule which has
        hte best similarity with user's input,
        """

        res,self.last_path = self.console.rule_match(speech, best_only=True)
        self.speech = speech
        self.domain_similarity,self.speech_domain,self.speech_matchee = res
        self._set_root_domain()

    def get_response(self, domain=None):
        """
        Generate a response to user's speech.
        Please note that this response is pre-defined in the json file,
        is not the result return by sub_module.
        """
        if domain is None:
            domain = self.speech_domain
        response = self.console.get_response(domain)

        if response is None:
            return "我猜你提的和「%s」有關, 不過目前還不知道該怎麼回應 :<" % self.speech_domain
        else:
            return response

    def _set_root_domain(self):

        """
        Extract the root rule in result.
        """
        if self.last_path == "":
            self.root_domain = self.speech_domain
        else:
            self.root_domain = self.last_path.split('>')[0]

    def get_task_handler(self, domain=None):

        """
        Get the instance of task handler based on the given domain.
        """

        if domain is None:
            domain = self.root_domain

        switch  = module_switch.Switch(self.console)
        handler = switch.get_handler(domain)

        return handler

if __name__ == '__main__':
    main()

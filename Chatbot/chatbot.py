# -*- coding: utf-8 -*-
import os
import random

import console
import task_modules.module_switch as module_switch
import RuleMatcher.customRuleBase as crb
import QuestionAnswering.qaBase as qa

class Chatbot(object):

    def __init__(self, name="MianBot", build_console=True):

        """
        # Args:
         - build_console: 是否要建構依照詞向量進行主題匹配的 console,
         如果只需要 qa 模組，可將 build_console 關閉，可見 demo_qa.py
        """

        self.name = name             # The name of chatbot.

        self.speech = ''             # The lastest user's input
        self.speech_domain = ''      # The domain of speech.
        self.speech_matchee = ''     # The matchee term of speech.
        self.speech_path = None      # The classification tree traveling path of speech.
        self.speech_seg = []

        self.root_domain = None      # The root domain of user's input.
        self.domain_similarity = 0.0 # The similarity between domain and speech.

        cur_dir = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        self.extract_attr_log = open('log/extract_arrt.log','w',encoding='utf-8')
        self.exception_log = open('log/exception.log','w',encoding='utf-8')
        os.chdir(cur_dir)

        if build_console:
            # For rule matching
            self.console = console.Console(model_path="model/ch-corpus-3sg.bin")
            self.custom_rulebase = crb.CustomRuleBase() # for one time matching.
            self.custom_rulebase.model = self.console.rb.model # pass word2vec model

        # For QA
        self.github_qa_unupdated = True
        if not self.github_qa_unupdated:
            self.answerer = qa.Answerer()

        self.default_response = [
            "是嗎?",
            "我不太明白你的意思",
            "原來如此"
        ]

    def waiting_loop(self):

        print("你好，我是 " + self.name)
        while True:

            speech = input()
            res = self.listen(speech)
            print(res[0])

    def listen(self, sentence, target=None, api_key=None, qa_threshold=35, qa_block_threshold=60):

        """
        listen function is to encapsulate the following getResponse methods:

            1.getResponseOnCustomDomain(sentence,api_key)
            2.getResponseOnRootDomains(sentence,target)
            3.getResponseForCustomQA(sentence,api_key)
            4.getResponseForGeneralQA(sentence)

        1,2 is to measure the consine similarity between keywords and sentence.
        3,4 is to measure the levenshtein distance between sentence and the questions
        in database/corpus.

        Args:
            - target : Optional. It is to define the user's input is in form of
            a sentence or a given answer by pressing the bubble buttom.
            If it is come from a button's text, target is the attribute name our
            module want to confirm.
            - api_key : for recognizing the user and get his custom rule/QAs.

        Return: [response,status,target,candiates]
            - response : Based on the result of modules or a default answer.
            - status   : It would be the module's current status if the user has
                         been sent into any module and had not left it.
            - target   : Refer to get_query() in task_modules/task.py
            - candiates: Refer to get_query() in task_modules/task.py
        """
        response = None
        stauts = None
        target = None
        candiates = None

        #FIXME
        # @zake7749
        # 區隔 custom rule 與 root rule 匹配的原因是 custom rule 並不支援多段式應答
        # 若後續在模組上進行更動，可考慮將兩者合併，透過辨識 api_key 的有無來修改操作

        # First of all,
        # Assume this sentence is for qa, but use a very high threshold.
        # FIXME Remove api_key TESTING VALUE
        qa_response, qa_sim = self.getResponseForQA(sentence,"TESTING",qa_threshold)
        if qa_sim > qa_block_threshold:
            return qa_response,None,None,None,None

        # matching on custom rules.
        # FIXME Remove api_key TESTING VALUE
        response = self.getResponseOnCustomDomain(sentence, api_key="TESTING")
        if response is not None:
            return response,None,None,None

        # if the confidence of the custom rule matching is too low,
        # do the original rule matching.
        is_confident = self.rule_match(sentence, threshold=0.4)

        if is_confident:
            response,stauts,target,candiates = self.getResponseOnRootDomains(target)
            return response,stauts,target,candiates

        # The result based on custom rules and general rules are not confident.
        # Assume that there are no intent in the sentence, consider this questions
        # is qa again, but this time use a smaller threshold.
        else:
            if qa_sim > qa_threshold:
                return qa_response,None,None,None
            else:
                # This query has too low similarity for all matching methods.
                # We can only send back a default response.
                return self.getDefaultResponse(),None,None,None

                #TODO
                # Use generative model to solve this case

    def getResponseOnRootDomains(self, target=None):

        """
        Send back a response and some history information based on the former
        result that came from rule_match().

        Args:
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

        handler = self._get_task_handler()

        try:
            status,response = handler.get_response(self.speech, self.speech_domain, target)
        except AttributeError:
            # It will happen when calling a module which have not implemented.
            # If you require more detailed information,
            # please refer module_switch.py and  task.py in the folder "task_modules".
            exception = "Handler of '%s' have not implemented" % self.root_domain
            print(exception)
            self.exception_log.write(exception)
            return [self.getDomainResponse(),None,None,None]

        if response is None:
            response = self.getDomainResponse()

        if status is None:
            # One pass talking, this sentence does not belong to any task.
            return [response,None,None,None]
        else:
            target,candiates = handler.get_query()
            handler.debug(self.extract_attr_log)
            return [response,status,target,candiates]

    def getResponseOnCustomDomain(self, sentence, api_key, threshold=.4):
        """
        Fetch user's custom rules by api_key and then match the sentence with
        custom rules.

        Args:
            - sentence: user's raw input. (not segmented)
            - api_key : a string to recognize the user and get rules defined by him/she.
            - threshold : a value between 0 to 1, to block the response which
              has a similarity lower than threshold.
        """
        if api_key is None:
            return None

        #TODO 調適為能夠進行「多段式對話」
        return self.custom_rulebase.customMatch(sentence, api_key, threshold)

    def getResponseForQA(self, sentence, api_key, threshold):
        """
        Encapsulate getResponseForGeneralQA, getResponseForCustomQA

        Return:
            - response, similarity
            if the similarity < threshold will return None,0.
        """

        #FIXME Remove this flag when all have done.
        if self.github_qa_unupdated:
            return None, 0

        # custom qa matching (with Fuzzy matching.)
        cqa_response,cqa_sim = self.getResponseForCustomQA(sentence,api_key)
        if cqa_sim > threshold:
            return cqa_response,cqa_sim

        # PTT qa matching (with bm25.)
        gqa_response,gqa_sim = self.getResponseForGeneralQA(sentence)
        if gqa_sim > threshold:
            return gqa_response,gqa_sim

        return None,0

    def getResponseForGeneralQA(self, sentence):

        """
        Listen user's input and return a response which is based on our
        knowledge base.

        Return:
            answer, similarity
        """
        if self.github_qa_unupdated:
            return None, 0

        return self.answerer.getResponse(sentence)

    def getResponseForCustomQA(self,sentence,api_key):

        """
        Listen user's input and return a response which is based on a cutsom
        knowledge base.

        Return:
            answer, similarity
        """
        if api_key is None:
            return None, 0

        return self.answerer.getResponse(sentence,api_key)

    def getLoggerData(self):
        return [self.root_domain,
                self.speech_domain,
                console.jieba.cut(self.speech,cut_all=False)]

    def rule_match(self, speech, threshold):

        """
        Set domain,path,similarity,root_domain based on the rule which has
        the best similarity with user's input.

        Return: a boolean value, to indicate that this match makes sense or not.
        """

        res,self.last_path = self.console.rule_match(speech, best_only=True)
        self.speech = speech
        self.domain_similarity,self.speech_domain,self.speech_matchee = res
        self._set_root_domain()

        if self.domain_similarity < threshold:
            return False
        else:
            return True

    def getDomainResponse(self, domain=None):
        """
        Generate a response to user's speech.
        Please note that this response is *pre-defined in the json file*,
        is not the result return by sub_module.
        """
        if domain is None:
            domain = self.speech_domain
        response = self.console.get_response(domain)
        return response

    def getDefaultResponse(self, query=None):

        """
        Send back a default response.
        """

        # TODO 根據 Query 的類型調整 default response
        # 如問句 -> 是嗎
        # 問關於 Chatbot 本身的行為 -> 別再提我的事了 etc
        # FIXME 這部分在銜接 Seqence to seqence 後將廢除

        return self.default_response[random.randrange(0,len(self.default_response))]

    def testQuestionAnswering(self, sentence):
        """
        專用於 QA 回覆，回傳(最佳回應、信心度)
        """
        # 默認 QA 庫，無閥值採用 BM25，關閉遠端 API
        if self.github_qa_unupdated:
            return ("Can not find the PTT CORPUS.",0)
        qa_response, qa_confidence = self.getResponseForGeneralQA(sentence)
        return (qa_response, qa_confidence)

    def testDomainAnswering(self):
        """
        專用於 Domain 的階層式匹配，回傳(模組回應、匹配路徑、信心度)
        """
        # 默認規則庫，無閥值，關閉遠端 API
        # @zake7749 沒有實現的必要性
        pass

    def testSeq2Seq(self):
        # TODO
        pass

    def _set_root_domain(self):

        """
        Extract the root rule in result.
        """
        if self.last_path == "":
            self.root_domain = self.speech_domain
        else:
            self.root_domain = self.last_path.split('>')[0]

    def _get_task_handler(self, domain=None):

        """
        Get the instance of task handler based on the given domain.
        """

        if domain is None:
            domain = self.root_domain

        switch  = module_switch.Switch(self.console)
        handler = switch.get_handler(domain)

        return handler

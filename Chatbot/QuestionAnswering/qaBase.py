import json

from .match import *
from .responsesEvaluate import Evaluator

class QABase(object):

    def __init__(self, data_path):

        """
        Args:
            data_path: 指出 data 資料夾位在哪個位置
        """
        self.general_questions = []
        self.data_path = data_path

        self.matcher = getMatcher(matcherType="Fuzzy")
        self.evaluator = Evaluator()

    def getResponse(self, sentence, api_key=None):

        if api_key is not None:
            response = self.getCustomQA(sentence,api_key)
        else:
            response = self._getGeneralQA(sentence)
        return response

    def getGeneralQA(self, sentence):

        pass

    def getCustomQA(self, sentence, api_key):

        #TODO GET USER'S QA BY api_key
        #customqa_list = json.loads(getUserQA(api_key))
        pass

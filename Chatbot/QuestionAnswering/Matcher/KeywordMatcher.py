from .matcher import Matcher

class KeywordMatcher(Matcher):

    """
    基於 TF-IDF 比較短語相似度
    """

    def __init__(self):

        self.vecModel = None
        #TODO

    def match(self, query):
        #TODO

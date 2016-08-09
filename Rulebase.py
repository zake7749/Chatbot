# -*- coding: utf-8 -*-

from gensim.models import word2vec
from gensim import models
import Rule

class RuleBase(object):
    """
    to store rules, and load the trained word2vec model.
    """
    def __init__(self, domain="general"):
        self.rules = []
        self.domain = domain

    def __str__(self):
        str = "Rules:\n------------\n"
        for rule in rules:
            str += str(rule)
            str += '\n'
        return str

    def rule_amount(self):
        return len(self.rules)

    def load_rules(self,path):
        """
        build the rulebase by loading the rules terms from given file.
        Data format is: Term1,Term2,Term3......

        Args: the path of file.
        """
        with open(path) as input:
            for line in input:
                rule_terms = line.strip('\n').split(' ')
                rule = Rule(self.rule_amount(), rule_terms, self.model)
                self.rules.append(rule)

    def load_model(self,path):
        """
        Load a trained word2vec model(binary format only).

        Args:
            path: the path of the model.
        """
        self.model = models.Word2Vec.load_word2vec_format(path,binary=True)

    def match(self, sentence, topk=1):
        """
        match the sentence with rules then order by similarity.

        Args:
            sentence: a list of words
        Return:
            a list hold top k-th rules.
        """
        result_list = []

        for rule in self.rules:
            result_list.append(rule.match(sentence))
        return result_list

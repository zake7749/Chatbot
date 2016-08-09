# -*- coding: utf-8 -*-

from gensim.models import word2vec
from gensim import models

class Rule(object):
    """
    Store the concept terms of a rule, and calculate the rule similarity.
    """

    def __init__(self, rule_id, rule_terms, word2vec_model):
        self.id    = rule_id
        self.terms = rule_terms
        self.model = word2vec_model

    def __str__(self):
        return ' '.join(self.terms)

    def match(self, sentence, threshold = 0):
        """
        Calculate the similarity between the input and concept terms.

        Args:
            threshold: a threshold to ignore the low similarity.
            sentence : a list of words.
        Returns:
            a struct : [similarity, [match_body]]
        """

        res = 0.0
        match_body = []

        for term in self.terms:
            max_sim = 0.0
            matchee = ""
            for word in sentence:
                try:
                    sim = self.model.similarity(term,word)
                    if sim > max_sim and sim > threshold:
                        matchee = word
                        max_sim = sim
                except Exception as e:
                    print(repr(e))

            res += max_sim
            match_body.append(matchee)
        return [res, str(self), match_body]

class RuleBase(object):
    """
    to store rules, and load the trained word2vec model.
    """
    def __init__(self, domain="general"):
        self.rules = []
        self.domain = domain
        self.model = None

    def __str__(self):
        res = "There are " + str(self.rule_amount()) + " rules in the rulebase:"
        res+= "\n--------------\n"
        end_index = self.rule_amount()-1

        for rule in self.rules[:end_index]:
            res += str(rule) + '\n'
        res += str(self.rules[end_index])
        return res

    def rule_amount(self):
        return len(self.rules)

    def load_rules(self,path):
        """
        build the rulebase by loading the rules terms from given file.
        Data format is: Term1,Term2,Term3......

        Args: the path of file.
        """
        assert self.model is not None, "Please load the model before matches."

        with open(path, 'r', encoding='utf-8') as input:
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

    def match(self, sentence, topk=1, threshold=0):
        """
        match the sentence with rules then order by similarity.

        Args:
            sentence: a list of words
            threshold: a threshold to ignore the low similarity.
        Return:
            a list hold top k-th rules.
        """
        assert self.model is not None, "Please load the model before matches."

        result_list = []

        for rule in self.rules:
            result_list.append(rule.match(sentence, threshold))
        topk = sorted(result_list, reverse=True , key=lambda k: k[0])
        return topk

# -*- coding: utf-8 -*-

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
            threshold: a threshold to block too low similarity.
            sentence : a list of words.
        Returns:
            a struct : [similarity, [match_body]]
        """

        res = 0.0
        max_sim = -1.0
        matchee = ""
        match_body = []

        for term in self.terms:
            for word in sentence:
                sim = self.model.similarity(term,word)
                if sim > max_sim and sim > threshold:
                    matchee = word
                    max_sim = sim
            res += max_sim
            match_body.append(matchee)
        return [res, match_body]

# -*- coding: utf-8 -*-
import os

from gensim.models import word2vec
from gensim import models

class Rule(object):
    """
    Store the concept terms of a rule, and calculate the rule similarity.
    """

    def __init__(self, rule_id, rule_terms, word2vec_model):
        self.id = rule_id
        self.id_term = rule_terms[0]
        self.terms = rule_terms
        self.model = word2vec_model
        self.children = []
        self.log = open('match.log','w', encoding='utf-8')

    def __str__(self):
        for term in self.terms:
            res = term
            if self.has_child():
                res += ' with children: '
                for child in self.children:
                    res += ' ' + str(child)
        return res

    def add_child(self,child_rule):
        """
        Add child rule into children list , e.g: Purchase(Parent) -> Drinks(Child).
        """
        self.children.append(child_rule)

    def has_child(self):
        return len(self.children)

    def match(self, sentence, threshold = 0):
        """
        Calculate the similarity between the input and concept term.

        Args:
            threshold: a threshold to ignore the low similarity.
            sentence : a list of words.
        Returns:
            a struct : [similarity, term_name, matchee in sentence]
        """

        max_sim = 0.0
        matchee = ""
        match_rule_term = ""

        for word in sentence:
            for term in self.terms:
                try:
                    sim = self.model.similarity(term,word)
                    if sim > max_sim and sim > threshold:
                        max_sim = sim
                        matchee = word
                except Exception as e:
                    print(repr(e)+ ". Try to hard-match.")
                    if term == word:
                        max_sim = 1
                        matchee = word

        return [max_sim, self.id_term, matchee]

class RuleBase(object):
    """
    to store rules, and load the trained word2vec model.
    """
    def __init__(self, domain="general"):
        self.rules = {}
        self.domain = domain
        self.model = None
        self.forest_base_roots = []

    def __str__(self):
        res = "There are " + str(self.rule_amount()) + " rules in the rulebase:"
        res+= "\n-------\n"
        for key,rulebody in self.rules.items():
            res += str(rulebody) + '\n'
        return res

    def rule_amount(self):
        return len(self.rules)

    def load_rules(self,path):
        """
        Build the rulebase by loading the rules terms from the given file.
        The data format is: child term, parent term(optional)

        Args: the path of file.
        """
        assert self.model is not None, "Please load the model before loading rules."
        self.rules.clear()

        with open(path, 'r', encoding='utf-8') as input:
            for line in input:
                rule_terms = line.strip('\n').split(' ')
                new_rule = Rule(self.rule_amount(), rule_terms[0].split(','), self.model)
                if new_rule.id_term not in self.rules:
                    self.rules[new_rule.id_term] = new_rule
                #else
                #    self.rules[new_rule.id_term].terms = rule_terms

                if len(rule_terms) > 1:
                    # this rule has parents.
                    for parent in rule_terms[1:]:
                        #if parent not in self.rules:
                        self.rules[parent].children.append(new_rule)
                else:
                    # is the root of classification tree.
                    self.forest_base_roots.append(new_rule)

    def load_rules_from_dic(self,path):
        """
        load all rule_files in given path
        """
        for file_name in os.listdir(path):
            self.load_rules(path + file_name)



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
            a list holds the top k-th rules and the classification tree travel path.
        """
        assert self.model is not None, "Please load the model before any match."

        result_list  = []
        at_leaf_node = False
        term_trans   = ""
        focused_rule = self.forest_base_roots[:]

        while not at_leaf_node:

            at_leaf_node = True

            for rule in focused_rule:
                result_list.append(rule.match(sentence, threshold))

            result_list = sorted(result_list, reverse=True , key=lambda k: k[0])
            top_domain  = result_list[0][1] # get the best matcher's term.

            if self.rules[top_domain].has_child():
                result_list = []
                term_trans += top_domain+'>'
                at_leaf_node = False
                focused_rule = self.rules[top_domain].children[:]

        return [result_list,term_trans]

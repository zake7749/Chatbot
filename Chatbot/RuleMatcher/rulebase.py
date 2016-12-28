# -*- coding: utf-8 -*-
import os
import json

from gensim.models import word2vec
from gensim import models

class Rule(object):
    """
    Store the concept terms of a rule, and calculate the rule similarity.
    """

    def __init__(self, domain, rule_terms, children, response, word2vec_model):

        self.id_term = domain
        self.terms = rule_terms
        self.model = word2vec_model
        self.response = response
        self.children = children

    def __str__(self):
        res = 'Domain:' + self.id_term
        if self.has_child():
            res += ' with children: '
            for child in self.children:
                res += ' ' + str(child)
        return res

    def serialize(self):
        """
        Convert the instance to json format.
        """
        ch_list = []
        for child in self.children:
            ch_list.append(child.id_term)

        cp_list = []
        for t in self.terms:
            cp_list.append(t)

        response = []

        data =  { "domain": str(self.id_term),
                  "concepts": cp_list,
                  "children": ch_list,
                  "response": response
                }
        return data

    def add_child(self,child_rule):
        """
        Add child rule into children list , e.g: Purchase(Parent) -> Drinks(Child).
        """
        self.children.append(child_rule)

    def has_child(self):
        return len(self.children)

    def has_response(self):
        return len(self.response)

    def match(self, sentence, threshold=0):
        """
        Calculate the similarity between the input and concept term.

        Args:
            threshold: a threshold to ignore the low similarity.
            sentence : a list of words.
        Returns:
            a struct : [similarity, domain_name, matchee in the sentence]
        """

        max_sim = 0.0
        matchee = ""

        for word in sentence:
            for term in self.terms:
                try:
                    sim = self.model.similarity(term,word)
                    if sim > max_sim and sim > threshold:
                        max_sim = sim
                        matchee = word
                except Exception as e:
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

    def output_as_json(self, path='rule.json'):

        rule_list = []
        for rule in self.rules.values():
            rule_list.append(rule.serialize())

        with open(path,'w',encoding='utf-8') as op:
            op.write(json.dumps(rule_list, indent=4))

    def load_rules_old_format(self,path):
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

    def load_rules(self, path, reload=False, is_root=False):
        """
        Build the rulebase by loading the rules terms from the given file.

        Args: the path of file.
        """
        assert self.model is not None, "Please load the model before loading rules."

        if reload:
            self.rules.clear()

        with open(path, 'r', encoding='utf-8') as input:
            json_data = json.load(input)
            # load rule and build an instance
            for data in json_data:

                domain = data["domain"]
                concepts_list = data["concepts"]
                children_list = data["children"]
                response = data["response"]

                if domain not in self.rules:
                    rule = Rule(domain, concepts_list, children_list, response, self.model)
                    self.rules[domain] = rule
                    if is_root:
                        self.forest_base_roots.append(rule)
                else:
                    print("[Rules]: Detect a duplicate domain name '%s'." % domain)


    def load_rules_from_dic(self,path):
        """
        load all rule_files in given path
        """
        for file_name in os.listdir(path):
            if not file_name.startswith('.'):  #escape .DS_Store on OSX.
                if file_name == "rule.json": # roots of forest
                    self.load_rules(path + file_name, is_root=True)
                else:
                    self.load_rules(path + file_name)


    def load_model(self,path):
        """
        Load a trained word2vec model(binary format only).

        Args:
            path: the path of the model.
        """
        self.model = models.Word2Vec.load_word2vec_format(path,binary=True)

    def match(self, sentence, topk=1, threshold=0, root=None):
        """
        match the sentence with rules then order by similarity.

        Args:
            sentence: a list of words
            threshold: a threshold to ignore the low similarity.
        Return:
            a list holds the top k-th rules and the classification tree travel path.
        """

        log = open("matching_log.txt",'w',encoding='utf-8')

        assert self.model is not None, "Please load the model before any match."

        result_list  = []
        at_leaf_node = False
        term_trans   = ""

        if root is None: # then search from roots of forest.
            focused_rule = self.forest_base_roots[:]
        else:
            focused_rule = [self.rules[root]]

        while not at_leaf_node:

            at_leaf_node = True

            for rule in focused_rule:
                result_list.append(rule.match(sentence, threshold))

            result_list = sorted(result_list, reverse=True , key=lambda k: k[0])
            top_domain  = result_list[0][1] # get the best matcher's term.

            #Output matching_log.
            log.write("---")
            for result in result_list:
                s,d,m = result
                log.write("Sim: %f, Domain: %s, Matchee: %s\n" % (s,d,m))
            log.write("---")


            if self.rules[top_domain].has_child():
                result_list = []
                term_trans += top_domain+'>'
                at_leaf_node = False

                # travel to the best node's children.
                focused_rule = []
                for rule_id in self.rules[top_domain].children:
                    focused_rule.append(self.rules[rule_id])
            else:
                term_trans += top_domain
        return [result_list,term_trans]

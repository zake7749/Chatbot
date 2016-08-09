# -*- coding: utf-8 -*-

import Rule
import RuleBase

def main():

    rulebase = RuleBase()
    rulebase.load_rules('rule.txt')
    rulebase.load_model('XXX.bin')

    res = rulebase.match(sentence)

if __name__ == '__main__':
    main()

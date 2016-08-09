# -*- coding: utf-8 -*-

import rule
import rulebase

def main():

    rb = rulebase.RuleBase()
    rb.load_rules('rule/rule.txt')
    print(rb)

if __name__ == '__main__':
    main()

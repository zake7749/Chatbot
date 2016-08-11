# -*- coding: utf-8 -*-

import jieba
import jieba.analyse

import rulebase

def main():

    init_jieba()
    sw = load_stopword()

    # build the rulebase
    rb = rulebase.RuleBase()
    rb.load_model('model/ch-corpus.bin')
    rb.load_rules('rule/baserule.txt')

    #into interactive console
    while True:
        show_information()
        choice = input('Your choice is: ')
        choice = choice.lower()
        if choice == 'e':
            res = jieba_tf_idf()
            for tag, weight in res:
                print('%s %s' % (tag, weight))
        elif choice == 'g':
            res = jieba_textrank()
            for tag, weight in res:
                print('%s %s' % (tag, weight))
        elif choice == 'p':
            print(rb)
        elif choice == 'r':
            rb.load_rules('rule/baserule.txt')
        elif choice == 't':
            test_speech(rb,sw)
        elif choice == 'm':
            speech = input('Input a sentence:')
            res,path = rule_match(rb,sw,speech)
            write_output(speech,res,path)
        elif choice == 'q':
            exit()
        else:
            print('[X] ' + choice + '.')

def jieba_textrank():
    speech = input('Input a sentence: ')
    return jieba.analyse.textrank(speech, withWeight=True, topK=20)

def jieba_tf_idf():
    speech = input('Input a sentence: ')
    return jieba.analyse.extract_tags(speech, topK=20, withWeight=True)

def show_information():
    print('Here is chat bot backend, echo your choice.')
    print('-------------------------------------------')
    print('E)xtract the name entity.')
    print('G)ive me the TextRank.')
    print('M)atch sentence with rules.')
    print('P)rint the rule in the rulebase.')
    print('R)eload the baserule.txt.')
    print('T)est the data in speech.txt.')
    print('Q)uit.')
    print('-------------------------------------------')

def init_jieba():
    #jieba custom setting
    #jieba.load_userdict("userdict.txt")
    jieba.set_dictionary('jieba_dict/dict.txt.big')

def load_stopword():
    #load stopword
    stopword = set()
    with open('jieba_dict/stopword.txt','r',encoding='utf-8') as stopword_list:
        for sw in stopword_list:
            sw = sw.strip('\n')
            stopword.add(sw)
    return stopword

def rule_match(rb, stopword, sentence):

    words = jieba.cut(sentence, HMM=False)
    #clean up the stopword
    keyword = []
    for word in words:
        if word not in stopword:
            keyword.append(word)

    return rb.match(keyword,threshold=0.1)

def test_speech(rb, stopword):

    output = open('test/output.txt','w',encoding='utf-8')
    # load sample data
    with open('test/speech.txt','r',encoding='utf-8') as input:
        for speech in input:
            speech = speech.strip('\n')
            result,path = rule_match(rb, stopword, speech)
            write_output(speech, result, path, output)

def write_output(org_speech, result, path, output = None):

    result_information = ''
    result_information += "Case# " + str(org_speech) + '\n'
    result_information += "------------------\n"
    for similarity,rule,matchee in result:
        str_sim = '%.4f' % similarity
        result_information += str_sim+'\t'+path+rule+'\t\t'+matchee+'\n'
    result_information += "------------------\n"

    if output is None:
        print(result_information)
    else:
        output.write(result_information)

if __name__ == '__main__':
    main()

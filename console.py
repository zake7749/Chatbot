# -*- coding: utf-8 -*-

import jieba

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
        if choice == 'p':
            print(rb)
        elif choice == 'r':
            rb.load_rules('rule/baserule.txt')
        else:
            test_speech(rb,sw)

def show_information():
    print('Here is chat bot backend, echo your choice.')
    print('-------------------------------------------')
    print('P)rint the rule in the rulebase.')
    print('R)eload the baserule.txt.')
    print('T)est the data in speech.txt.')
    print('-------------------------------------------')

def init_jieba():
    #jieba custom setting
    #jieba.load_userdict("userdict.txt") TODO
    jieba.set_dictionary('jieba_dict/dict.txt.big')

def load_stopword():
    #load stopword
    stopword = set()
    with open('jieba_dict/stopword.txt','r',encoding='utf-8') as stopword_list:
        for sw in stopword_list:
            sw = sw.strip('\n')
            stopword.add(sw)
    return stopword

def test_speech(rb,stopword):

    output = open('test/output.txt','w',encoding='utf-8')
    # load sample data
    with open('test/speech.txt','r',encoding='utf-8') as input:
        for speech in input:
            speech = speech.strip('\n')
            sentence = jieba.cut(speech, HMM=False)

            #clean up the stopword
            keyword = []
            for word in sentence:
                if word not in stopword:
                    keyword.append(word)

            result,path = rb.match(keyword,threshold=0.1)

            output.write("Case# " + str(speech) + '\n')
            output.write("------------------\n")
            for similarity,rule,matchee in result:
                str_sim = '%.4f' % similarity
                output.write(str_sim+'\t'+path+rule+'\t\t'+matchee+'\n')
            output.write("------------------\n")

if __name__ == '__main__':
    main()

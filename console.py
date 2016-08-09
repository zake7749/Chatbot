# -*- coding: utf-8 -*-

import jieba

import rulebase

def main():

    #jieba custom setting
    #jieba.load_userdict("userdict.txt") TODO
    jieba.set_dictionary('jieba_dict/dict.txt.big')
    jieba.suggest_freq('訂',True)
    jieba.suggest_freq('幫',True)
    jieba.suggest_freq(('能','幫'),True)
    jieba.suggest_freq(('訂','個'),True)
    jieba.suggest_freq(('我','訂'),True)
    jieba.suggest_freq(('買','些'),True)


    #load stopword
    stopword = set()
    with open('jieba_dict/stopword.txt','r',encoding='utf-8') as stopword_list:
        for sw in stopword_list:
            sw = sw.strip('\n')
            stopword.add(sw)

    # build the rulebase
    rb = rulebase.RuleBase()
    rb.load_model('model/ch-corpus.bin')
    rb.load_rules('rule/baserule.txt')

    output = open('test/output.txt','w',encoding='utf-8')

    # load sample data
    with open('test/speech.txt','r',encoding='utf-8') as input:
        for speech in input:
            speech = speech.strip('\n')
            sentence = jieba.cut(speech, HMM=False)

            keyword = []
            for word in sentence:
                if word not in stopword:
                    keyword.append(word)

            result = rb.match(keyword,threshold=0.26)

            output.write("Case# " + str(speech) + '\n')
            output.write("------------------\n")
            for similarity,rule,matchee in result:
                output.write(str(similarity)+'\t'+rule+'\t'+str(matchee)+'\n')
            output.write("------------------\n")
    print(rb)

if __name__ == '__main__':
    main()

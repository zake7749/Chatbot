# -*- coding: utf-8 -*-

import jieba
import jieba.analyse
import RuleMatcher.rulebase as rulebase

def main():
    console = Console()
    console.listen()


class Console(object):

    def __init__(self,model_path="model/ch-corpus.bin",
                 rule_path="RuleMatcher/rule/rule.json",
                 stopword="jieba_dict/stopword.txt",
                 jieba_dic="jieba_dict/dict.txt.big",
                 jieba_user_dic="jieba_dict/userdict.txt"):
        print("Building a console...")

        # jieba custom setting.
        self.init_jieba(jieba_dic, jieba_user_dic)
        self.stopword = self.load_stopword(stopword)

        # build the rulebase.
        self.rb = rulebase.RuleBase()
        self.rb.load_model(model_path)
        self.rb.load_rules(rule_path)

    def listen(self):
        #into interactive console
        while True:
            self.show_information()
            choice = input('Your choice is: ')
            choice = choice.lower()
            if choice == 'e':
                res = self.jieba_tf_idf()
                for tag, weight in res:
                    print('%s %s' % (tag, weight))
            elif choice == 'g':
                res = self.jieba_textrank()
                for tag, weight in res:
                    print('%s %s' % (tag, weight))
            elif choice == 'p':
                print(self.rb)
            elif choice == 'r':
                self.rb.load_rules('rule/baserule.txt')
            elif choice == 't':
                self.test_speech()
            elif choice == 'm':
                speech = input('Input a sentence:')
                res,path = self.rule_match(speech)
                self.write_output(speech,res,path)
            elif choice == 'b':
                exit()
            elif choice == 'o':
                self.rb.output_to_json()
            else:
                print('[Opps!] No such choice: ' + choice + '.')

    def jieba_textrank(self):
        """
        Use textrank in jieba to extract keywords in a sentence.
        """
        speech = input('Input a sentence: ')
        return jieba.analyse.textrank(speech, withWeight=True, topK=20)

    def jieba_tf_idf(self):
        """
        Use tf/idf in jieba to extract keywords in a sentence
        """
        speech = input('Input a sentence: ')
        return jieba.analyse.extract_tags(speech, topK=20, withWeight=True)

    def show_information(self):
        print('Here is chat bot backend, enter your choice.')
        print('-------------------------------------------')
        print('E)xtract the name entity.')
        print('G)ive me the TextRank.')
        print('M)atch sentence with rules.')
        print('P)rint the rule in the rulebase.')
        print('R)eload the baserule.txt.')
        print('T)est the data in speech.txt.')
        print('B)ye.')
        print('-------------------------------------------')

    def init_jieba(self, seg_dic, userdic):

        """
        jieba custom setting.
        """
        jieba.load_userdict(userdic)
        jieba.set_dictionary(seg_dic)
        with open(userdic,'r',encoding='utf-8') as input:
            for word in input:
                word = word.strip('\n')
                jieba.suggest_freq(word, True)

    def load_stopword(self, path):

        stopword = set()
        with open(path,'r',encoding='utf-8') as stopword_list:
            for sw in stopword_list:
                sw = sw.strip('\n')
                stopword.add(sw)
        return stopword

    def rule_match(self, sentence):

        """
        Match the sentence with rules.
        """

        words = jieba.cut(sentence, HMM=False)
        #clean up the stopword
        keyword = []
        for word in words:
            if word not in self.stopword:
                keyword.append(word)

        return self.rb.match(keyword,threshold=0.1)

    def test_speech(self):

        """
        Try matching all sentence in 'example/output.txt'
        """

        output = open('example/output.txt','w',encoding='utf-8')
        # load sample data
        with open('example/speech.txt','r',encoding='utf-8') as input:
            for speech in input:
                speech = speech.strip('\n')
                result,path = self.rule_match(speech)
                self.write_output(speech, result, path, output)

    def write_output(self, org_speech, result, path, output = None):

        """
        Show the matching result.

            Args:
                - org_speech: the original input string.
                - result: a sorted array, refer match() in rulebase.py.
                - path: the travel path in classification tree.
                - output: expect as a file writer, if none, print
                  the result to stdio.
        """
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

import math
import logging

import gensim

from collections import defaultdict

from .matcher import Matcher

class WordWeightMatcher(Matcher):

    """
    採用詞權重來比對短語相似度
    """

    def __init__(self, segLib="Taiba"):

        super().__init__(segLib)

        self.wordDictionary = defaultdict(int) # 保存每個詞的出現次數
        self.totalWords = 0 # 詞總數
        self.wordWeights = defaultdict(int) # 保存每個詞的權重

    def initialize(self):
        logging.info("初始化模塊中...")
        self.TitlesSegmentation()
        self.buildWordDictionary()
        self.loadStopWords("data/stopwords/chinese_sw.txt")
        self.loadStopWords("data/stopwords/specialMarks.txt")
        self.calculateWeight()
        logging.info("初始化完成 :>")

    def buildWordDictionary(self):

        for title in self.segTitles:
            for word in title:
                self.wordDictionary[word] += 1
                self.totalWords += 1
        logging.info("詞記數完成")

    def buildWordBag(self):
        dictionary = gensim.corpora.Dictionary(self.titles)

    def calculateWeight(self):
        # 算法的數學推導請見：
        # 非主流自然语言处理——遗忘算法系列（四）：改进TF-IDF权重公式
        # http://www.52nlp.cn/forgetnlp4
        # 此處儲存的 weight 為後項，即 -1 * log(N/T)

        for word,count in self.wordDictionary.items():
            self.wordWeights[word] = -1 * math.log10(count/self.totalWords)
        logging.info("詞統計完成")

    def getCooccurrence(self, q1, q2):

        #TODO NEED OPTIMIZE!!!!
        res = []
        for word in q1:
            if word in q2:
                res.append(word)
        return res

    def getWordWeight(self, word, n=1):
        #TODO FIX N
        return(n * self.wordWeights[word])

    def match(self, query, sort=False):

        """
        讀入使用者 query，若語料庫中存在相同的句子，便回傳該句子與標號
        """

        max_similarity = -1
        target = ""
        index = -1

        segQuery = [word for word in self.wordSegmentation(query)
                    if word not in self.stopwords]

        for index,title in enumerate(self.segTitles):

            if len(title) == 0:
                continue

            allWordsWeight = 0.
            coWordsWeight = 0.

            coWords = self.getCooccurrence(title, segQuery)

            for word in coWords:
                coWordsWeight += self.getWordWeight(word)

            for word in title:
                if word not in coWords:
                    allWordsWeight += self.getWordWeight(word)
            for word in segQuery:
                if word not in coWords:
                    allWordsWeight += self.getWordWeight(word)
            similarity = coWordsWeight/allWordsWeight

            if similarity > max_similarity:
                max_similarity = similarity
                target = title
                target_idx = index

        self.similarity = max_similarity * 100 #統一為百分制

        return target,target_idx

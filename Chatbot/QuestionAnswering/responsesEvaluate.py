import logging
import os
import math

from collections import defaultdict

from gensim import corpora

# 引入斷詞與停用詞的配置
from .Matcher.matcher import Matcher

class Evaluator(Matcher):
    """
    讀入一串推文串列，計算出當中可靠度最高的推文
    """
    def __init__(self,segLib="Taiba"):

        #FIXME 若「線上版本」受記憶體容量限制，需考慮更換為 jieba!
        super().__init__(segLib)
        self.responses = []
        self.segResponses = []
        self.totalWords = 0

        self.path = os.path.dirname(__file__)
        self.debugLog = open(self.path + "/data/EvaluateLog.txt",'w',encoding="utf-8")

        self.filteredWords = set() # 必須濾除的回應

        self.counterDictionary = defaultdict(int) # 用於統計詞頻
        self.tokenDictionary = None # 用於分配詞 id，與建置詞袋

        # 中文停用詞與特殊符號加載
        self.loadStopWords(path=self.path + "/data/stopwords/chinese_sw.txt")
        self.loadStopWords(path=self.path + "/data/stopwords/specialMarks.txt")
        self.loadFilterdWord(path=self.path + "/data/stopwords/ptt_words.txt")

    def cleanFormerResult(self):
        """
        清空之前回應留下的紀錄
        """
        self.responses = []
        self.segResponses = []
        self.totalWords = 0

    def getBestResponse(self, responses, topk, debugMode=False):
        """
        從 self.responses 中挑選出可靠度前 K 高的回應回傳

        Return : List of (reply,grade)
        """
        self.cleanFormerResult()

        self.buildResponses(responses)
        self.segmentResponse()
        self.buildCounterDictionary()
        candiateList = self.evaluateByGrade(topk, debug=debugMode)

        return candiateList

    def loadFilterdWord(self,path):
        with open(path, 'r', encoding='utf-8') as sw:
            for word in sw:
                self.filteredWords.add(word.strip('\n'))

    def buildResponses(self, responses):
        """
        將 json 格式中目前用不上的 user,vote 去除，只留下 Content
        """
        self.responses = []
        for response in responses:
            clean = True
            r = response["Content"]
            for word in self.filteredWords:
                if word in r:
                    clean = False
            if clean:
                self.responses.append(response["Content"])

    def segmentResponse(self):
        """
        對 self.responses 中所有的回應斷詞並去除中文停用詞，儲存於 self.segResponses
        """
        self.segResponses = []
        for response in self.responses:
            keywordResponse = [keyword for keyword in self.wordSegmentation(response)
                               if keyword not in self.stopwords
                               and keyword != ' ']
            self.totalWords += len(keywordResponse)
            self.segResponses.append(keywordResponse)
        #logging.info("已完成回應斷詞")

    def buildCounterDictionary(self):
        """
        統計 self.segResponses 中每個詞出現的次數
        """
        for reply in self.segResponses:
            for word in reply:
                self.counterDictionary[word] += 1
        #logging.info("計數字典建置完成")

    def buildTokenDictionary(self):
        """
        為 self.segResponses 中的詞配置一個 id
        """
        self.tokenDictionary = corpora.Dictionary(self.segResponses)
        logging.info("詞袋字典建置完成，%s" % str(self.tokenDictionary))

    def evaluateByGrade(self,topk,debug=False):
        """
        依照每個詞出現的在該文件出現的情形，給予每個回覆一個分數
        若該回覆包含越多高詞頻的詞，其得分越高

        Args:
            - 若 debug 為 True，列出每筆評論的評分與斷詞情形

        Return: (BestResponse,Grade)
            - BestResponse: 得分最高的回覆
            - Grade: 該回覆獲得的分數
        """
        bestResponse = ""
        candiates = []

        avgWords = self.totalWords/len(self.segResponses)

        for i in range(0, len(self.segResponses)):

            wordCount = len(self.segResponses[i])
            sourceCount = len(self.responses[i])
            meanful = 0

            if wordCount == 0 or sourceCount > 24:
                continue

            cur_grade = 0.

            for word in self.segResponses[i]:
                wordWeight = self.counterDictionary[word]
                if wordWeight > 1:
                    meanful += math.log(wordWeight,10)
                cur_grade += wordWeight

            cur_grade = cur_grade * meanful / (math.log(len(self.segResponses[i])+1,avgWords) + 1)
            candiates.append([self.responses[i],cur_grade])

            if debug:
                result = self.responses[i] + '\t' + str(self.segResponses[i]) + '\t' + str(cur_grade)
                self.debugLog.write(result+'\n')
                print(result)

        candiates = sorted(candiates,key=lambda candiate:candiate[1],reverse=True)
        return candiates[:topk]

class ClusteringEvaluator(Evaluator):
    """
    基於聚類評比推文可靠度
    """
    pass

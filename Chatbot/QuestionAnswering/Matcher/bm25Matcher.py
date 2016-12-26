import math

from .matcher import Matcher
from .quickSearch import QuickSearcher


class bestMatchingMatcher(Matcher):

    """
    基於 bm25 算法取得最佳關聯短語
    """

    def __init__(self, segLib="Taiba", removeStopWords=False):
        super().__init__(segLib)

        self.cleanStopWords = removeStopWords
        self.D = 0 # 句子總數

        self.wordset = set() # Corpus 中所有詞的集合
        self.words_location_record = dict()  # 紀錄該詞 (key) 出現在哪幾個句子(id)
        self.words_idf = dict() # 紀錄每個詞的 idf 值

        self.f = []
        self.df = {}
        self.idf = {}
        self.k1 = 1.5
        self.b = 0.75

        self.searcher = QuickSearcher() # 問句篩選

        if removeStopWords:
            self.loadStopWords("data/stopwords/chinese_sw.txt")
            self.loadStopWords("data/stopwords/specialMarks.txt")

    def initialize(self,ngram=1):

        assert len(self.titles) > 0, "請先載入短語表"

        self.TitlesSegmentation() # 將 self.titles 斷詞為  self.segTitles
        #self.calculateIDF() # 依照斷詞後結果, 計算每個詞的 idf value
        self.initBM25()
        self.searcher.buildInvertedIndex(self.segTitles)

        """NEED MORE DISCUSSION
        #for n in range(0,ngram):
        #    self.addNgram(n)
        """

    def initBM25(self):

        print("BM25模塊初始化中")

        self.D = len(self.segTitles)
        self.avgdl = sum([len(title) + 0.0 for title in self.segTitles]) / self.D

        for seg_title in self.segTitles:
            tmp = {}
            for word in seg_title:
                if not word in tmp:
                    tmp[word] = 0
                tmp[word] += 1
            self.f.append(tmp)
            for k, v in tmp.items():
                if k not in self.df:
                    self.df[k] = 0
                self.df[k] += 1
        for k, v in self.df.items():
            self.idf[k] = math.log(self.D-v+0.5)-math.log(v+0.5)

        print("BM25模塊初始化完成")

    def sim(self, doc, index):
        score = 0
        for word in doc:
            if word not in self.f[index]:
                continue
            d = len(self.segTitles[index])
            score += (self.idf[word]*self.f[index][word]*(self.k1+1)
                      / (self.f[index][word]+self.k1*(1-self.b+self.b*d
                                                      / self.avgdl)))
        return score

    def calculateIDF(self):

        # 構建詞集與紀錄詞出現位置的字典
        if len(self.wordset) == 0:
            self.buildWordSet()
        if len(self.words_location_record) == 0:
            self.buildWordLocationRecord()

        # 計算 idf
        for word in self.wordset:
            self.words_idf[word] = math.log2((self.D + .5)/(self.words_location_record[word] + .5))


    def buildWordLocationRecord(self):
        """
        建構詞與詞出現位置（句子id）的字典
        """
        for idx,seg_title in enumerate(self.segTitles):
            for word in seg_title:
                if self.words_location_record[word] is None:
                    self.words_location_record[word] = set()
                self.words_location_record[word].add(idx)

    def buildWordSet(self):
        """
        建立 Corpus 詞集
        """
        for seg_title in self.segTitles:
            for word in seg_title:
                self.wordset.add(word)

    def addNgram(self,n):
        """
        擴充 self.seg_titles 為 n-gram
        """
        idx = 0

        for seg_list in self.segTitles:
            ngram = self.generateNgram(n,self.titles[idx])
            seg_list = seg_list + ngram
            idx += 1

    def generateNgram(self,n,sentence):
        return [sentence[i:i+n] for i in range(0,len(sentence)-1)]


    def joinTitles(self):
        self.segTitles = ["".join(title) for title in self.segTitles]

    def match(self, query):
        """
        讀入使用者 query，若語料庫中存在類似的句子，便回傳該句子與標號

        Args:
            - query: 使用者欲查詢的語句
        """

        seg_query = self.wordSegmentation(query)
        max = -1
        target = ''
        target_idx = -1

        target_index = self.searcher.quickSearch(seg_query) #  只取出必要的 titles

        for index in target_index:
            score = self.sim(seg_query, index)
            if score > max:
                target_idx = index
                max = score

        # normalization
        max = max / self.sim(self.segTitles[target_idx],target_idx)
        target = ''.join(self.segTitles[target_idx])
        self.similarity = max * 100 #百分制

        return target,target_idx

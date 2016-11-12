from .matcher import Matcher
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class FuzzyMatcher(Matcher):

    """
    基於萊文斯坦距離比對短語相似度
    """

    def __init__(self, segLib="Taiba", removeStopWords=False):
        super().__init__(segLib)
        self.cleanStopWords = removeStopWords
        if removeStopWords:
            self.loadStopWords("data/stopwords/chinese_sw.txt")
            self.loadStopWords("data/stopwords/specialMarks.txt")

    def joinTitles(self):
        self.segTitles = ["".join(title) for title in self.segTitles]

    def tieBreak(self, query, i, j):
        """
        當去除停用詞後導致兩個字串的匹配度一樣時，從原文裡挑選出更適合的

        Args:
            - query: 使用者的輸入
            - i: index 為 i 的 title
            - j: index 為 j 的 title

        Return: (target, index)
            - target: 較適合的標題
            - index : 該標題的 id
        """
        raw1 = self.titles[i]
        raw2 = self.titles[j]

        r1 = fuzz.ratio(query, raw1)
        r2 = fuzz.ratio(query, raw2)

        if r1 > r2:
            return (raw1,i)
        else:
            return (raw2,j)

    def match(self, query, custom_title=None):
        """
        讀入使用者 query，若語料庫中存在類似的句子，便回傳該句子與標號

        Args:
            - query: 使用者欲查詢的語句
            - removeStopWords: 清除 stopwords
            - custom_title: 使用者欲比對的問題集
        """
        ratio  = -1
        target = ""
        target_idx = -1

        if self.cleanStopWords:
            mQuery = [word for word in self.wordSegmentation(query)
                      if word not in self.stopwords]
            mQuery = "".join(mQuery)
            title_list = self.segTitles
        else:
            if custom_title is None:
                title_list = self.titles
            else:
                title_list = custom_title
            mQuery = query

        for index,title in enumerate(title_list):

            newRatio = fuzz.ratio(mQuery, title)

            if newRatio > ratio:
                ratio  = newRatio
                target = title
                target_idx = index

            elif self.cleanStopWords and newRatio == ratio:
                target, target_idx = self.tieBreak(query,target_idx,index)

        self.similarity = ratio
        return target,target_idx

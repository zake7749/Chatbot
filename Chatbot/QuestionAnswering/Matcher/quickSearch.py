class QuickSearcher(object):

    """
    對每個句子的詞建立反向映射表，透過 set operator 快速限縮查詢時間
    """

    def __init__(self, docs=None):

        self.inverted_word_dic = dict()
        #self.buildInvertedIndex(docs)

    def buildInvertedIndex(self, docs):

        """
        建構詞對 ID 的倒排索引

        Args:
            - docs: 欲建構的倒排索引表列，每個 doc 需「完成斷詞」
        """

        for doc_id,doc in enumerate(docs):
            for word in doc:
                if word not in self.inverted_word_dic.keys():
                    self.inverted_word_dic[word] = set()
                self.inverted_word_dic[word].add(doc_id)

    def quickSearch(self, query):

        """
        讀入已斷好詞的 query，依照倒排索引只取出必要的 id
        """

        result = set()
        # print(query)
        for word in query:
            if word in self.inverted_word_dic.keys():
                result = result.union(self.inverted_word_dic[word])

        return result

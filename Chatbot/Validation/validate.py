
class Validator(object):

    """
    用於驗證預設匹配結果與實際匹配結果是否有不同
    """

    def __init__(self):
        self.paths = []
        self.sentences = []

    def loadValiadationData(self, paths_datapath, sentences_datapath):

        self.loadPaths(paths_datapath)
        self.loadSentences(sentences_datapath)

    def loadPaths(self, path):
        with open(path,'r',encoding='utf-8') as input:
            self.paths = [line.strip('\n') for line in input]

    def loadSentences(self, path):
        with open(path,'r',encoding='utf-8') as input:
            self.sentences = [line.strip('\n') for line in input]

    def validate(self, match, root_only=False):

        """
        # TODO APPEND TO TRAINING MODULE
        驗證預設分類結果與實際分類結果

        Args:
            # match:用於比對的函式，建議採用 console.match，該函式
            # 需要回傳匹配路徑與匹配相似度

        Return : 誤分點的總數,點的評比表列
        """

        miss = 0
        categorical_matrix = []

        for i in range(0,len(self.sentences)):
            for sentence in self.sentences:
                sim,path = match(sentence)
                if root_only:
                    #TODO
                    pass
                else:
                    if path != self.paths[i]:
                        miss += 1
                        categorical_matrix.append(1)
                        print("在'%s'中,預期為 %s,實際為 %s" % (sentence,self.paths[i],path))
                    else:
                        categorical_matrix.append(0)
        return (miss, categorical_matrix)

class Symptom(object):

    def __init__(self,name):
        self.name = name
        self.weight = 0.0
        self.talks = "" # 症狀的口語描述
        self.diseases = None # 一個症狀對應的可能疾病集
        self.toggle = False # 標記症狀是否已被詢問過

    def __str__(self):
        res =  self.name + " with weight: " + str(self.weight) + "\ndescription: " + self.talks
        res +=  "\n with disease:"

        assert self.diseases is not None, "Symptom is unintialized !"
        for disease in self.diseases:
            res += disease + '\t'
        return res

    def to_json(self):

        res = {
            "name": str(self.name),
            "weight": float(self.weight),
            "talks": str(self.talks),
            "diseases": list(self.diseases)
        }
        return res

class Disease(object):

    def __init__(self,name):
        self.name = name
        self.department = ''
        self.bias  = 0.0 # 基礎偏差，與該疾病發生的頻率有關
        self.grade = 0.0
        self.symptom = set()

    def __str__(self):
        return self.name + " 科別為:" + self.department + ". bias = " + str(self.bias) + ". grade = " + str(self.grade)

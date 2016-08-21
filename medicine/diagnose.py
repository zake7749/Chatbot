import sys
import os

import symptom
import disease
from toolkit import cleanline

def main():

    doctor = Doctor()
    doctor.diagnose(sys.argv[1])

class Doctor(object):

    def __init__(self):
        self.symptoms_dic = self.get_symptoms_knowledge()
        self.diseases_dic = self.get_diseases_knowledge()

    def get_symptoms_knowledge(self):
        """回傳一個症狀對應疾病，與症狀分數和症狀描述的結構
        """
        dic = {}

        # load symptom disease pair
        abs_path = os.path.join(os.path.dirname(__file__) + 'result/sdpair')
        with open(abs_path,'r',encoding='utf-8') as input:
            for line in input:
                line = cleanline(line)
                sym_term = line.split(':')[0]
                dic[sym_term] = symptom.Symptom(sym_term)
                dic[sym_term].diseases = set(line.split(':')[1].split(','))
        # load symptom's weight.
        abs_path = os.path.join(os.path.dirname(__file__) + 'result/symptom_score.txt')
        with open(abs_path,'r',encoding='utf-8') as input:
            for line in input:
                line = cleanline(line)
                sym_term = line.split(':')[0]
                dic[sym_term].weight = float(line.split(':')[1])
        # load symptom's description.
        abs_path = os.path.join(os.path.dirname(__file__) + 'result/symptom_talks.txt')
        with open(abs_path,'r',encoding='utf-8') as input:
            for line in input:
                line = cleanline(line)
                sym_term = line.split(':')[0]
                dic[sym_term].talks = line.split(':')[1]
        return dic

    def get_diseases_knowledge(self):
        """回傳一個疾病、科別與疾病分數的結構
        """
        dic = {}

        abs_path = os.path.join(os.path.dirname(__file__) + 'result/ddpair')
        # load department of disease
        with open(abs_path,'r',encoding='utf-8') as input:
            for line in input:
                line = cleanline(line)
                dis_term = line.split(':')[0]
                dic[dis_term] = disease.Disease(dis_term)
                dic[dis_term].department = line.split(':')[1]
        # load bias
        abs_path = os.path.join(os.path.dirname(__file__) + 'result/disease_bias.txt')
        with open(abs_path,'r',encoding='utf-8') as input:
            for line in input:
                line = cleanline(line)
                dis_term = line.split(':')[0]
                dic[dis_term].bias  = float(line.split(':')[1])
                dic[dis_term].grade = dic[dis_term].bias
        return dic

    def clear_disease_grade(self):
        """重新設定每一個疾病的 grade
        """
        for disease in self.diseases_dic.values():
            disease.grade = disease.bias

    def clear_symptom_toggle(self):
        """將每一個症狀的使用標記清空
        """
        for symptom in self.symptoms_dic.values():
            symptom.toggle = False

    def evaluate(self, symptom, flag):
        """傳入一個症狀，依疾病是否有出現該症狀來調整該病的得分

            Args:
                - flag: 表示病人是否有出現該症狀.
                - symptom: 欲檢測的症狀字串.
        """
        symptom_inst = self.symptoms_dic[symptom]
        symptom_inst.toggle = True # 標記該症狀已被求值

        flag = int(flag)

        for disease in self.diseases_dic.values():

            try:
                disease_weight = 1.5/(len(self.get_symptom(disease.name))+1)

                if disease.name in symptom_inst.diseases and flag == 1:
                    disease.grade += symptom_inst.weight * disease_weight
                elif disease.name not in symptom_inst.diseases and flag == 1:
                    disease.grade -= symptom_inst.weight * disease_weight
            except Exception as e:
                print('[Error]' + str(disease))
                print(e)
    def diagnose(self, description, depth=10):
        """依照症狀與疾病的對應字典來判斷可能疾病

            Args:
                - description: 一個症狀與該症出現與否的字串
                - depth: an int. 用於決定問診次數
        """

        if description == '':
            query = input('Initialize with some symptoms(split by ","): ')

        # 照格式取出元素
        symptoms = self.parse_input(description)

        # 初始化疾病成績，清空已存的症狀標記
        self.clear_disease_grade()
        self.clear_symptom_toggle()

        # 進入診斷迴圈
        while depth != 0:
            depth -= 1
            for symptom,flag in symptoms:
                self.evaluate(symptom,flag) # 依症狀出現與否給疾病打分
            cache = sorted(self.diseases_dic.values(), key=lambda disease: disease.grade, reverse=True)
            target_sym, query  = self.get_query(cache,10) # 詢問下一個症狀是否出現
            choice = input(query)
            symptoms = [[target_sym,choice]] # 依 choice 更新患者症狀

        # 列出診斷結果
        for d in cache[:30]:
            print(d)


    def parse_input(self, description):
        """分拆讀入字串，回傳一個(症狀,出現與否)的列表

            Args:
                - description: 欲解析的字串
        """
        res = []
        ds = description.split(',')
        for d in ds:
            res.append(d.split('#'))
        return res

    def get_query(self, diseases, topk=30):
        """依照目前答案集回傳可最佳分割的症狀與其症狀描述

            Args:
                - disease: a list. 已照 grade 排序的疾病.
                - topk: an int. 表要列入計算分割點前 k 個疾病.
        """

        symptom_counter = {} # 存放症狀與症狀出現筆數

        # 計算前 topk 個疾病的症狀分佈
        for disease in diseases[:topk]:
            print(disease)
            syms_of_dis = self.get_symptom(disease.name)
            for symptom in syms_of_dis:
                if not self.symptoms_dic[symptom].toggle: #（該症狀是未被詢問過的）
                    symptom_counter[symptom] = symptom_counter.get(symptom,0) + 1

        symptom_counter = sorted(symptom_counter.keys(), key=lambda k:symptom_counter[k], reverse=True)
        #target = symptom_counter[int(len(symptom_counter)/2)] #取出中間值視為最優分割點
        print(symptom_counter)
        target = symptom_counter[0]
        return [target,self.symptoms_dic[target].talks]


    def get_symptom(self, disease):
        """傳入一個疾病，取得這個疾病的所有症狀
        """
        sym_list = []
        for symptom in self.symptoms_dic.values():
            if disease in symptom.diseases:
                sym_list.append(symptom.name)
        return sym_list

if __name__ == '__main__':
    main()

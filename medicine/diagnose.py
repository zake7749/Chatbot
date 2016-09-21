import sys
import os
import random

import symptom
import disease
from toolkit import cleanline

def main():

    doctor = Doctor(False)
    res = doctor.get_disease_with_maxs()
    #print(str(res))
    #print(doctor.get_symptom(res[1]))
    doctor.diagnose(sys.argv[1])

class Doctor(object):

    def __init__(self, is_girl):
        self.symptoms_dic = self.get_symptoms_knowledge()
        self.diseases_dic = self.get_diseases_knowledge()
        self.is_girl = is_girl

    def get_symptoms_knowledge(self):
        """回傳一個症狀對應疾病，與症狀分數和症狀描述的結構
        """
        dic = {}

        # load symptom disease pair
        abs_path = os.path.join(os.path.dirname(__file__) + 'result/sdpair.txt')
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

    def get_disease_with_maxs(self):
        """回傳一個由症狀最多的疾病，以及其疾病數的列表
        """
        max = -1
        res = []
        for disease in self.diseases_dic.keys():
            num = len(self.get_symptom(disease))
            if max < num:
                max = num
                res = [max, disease]
        return res

    def get_diseases_knowledge(self):
        """回傳一個疾病、科別與疾病分數的結構
        """
        dic = {}

        abs_path = os.path.join(os.path.dirname(__file__) + 'result/ddpair.txt')
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
        symptom_inst.toggle = True # 標記已被使用過（針對初始化）

        flag = int(flag)

        for disease in self.diseases_dic.values():

            try:
                #disease_weight = 14/(len(self.get_symptom(disease.name))+1)
                disease_weight = 1

                if disease.name in symptom_inst.diseases and flag == 1:
                    disease.grade += symptom_inst.weight * disease_weight
                elif disease.name not in symptom_inst.diseases and flag == 1:
                    disease.grade -= symptom_inst.weight * disease_weight
            except Exception as e:
                print('[Error]' + str(disease))
                print(e)

    def diagnose(self, description, depth=6):
        """依照症狀與疾病的對應字典來判斷可能疾病

            Args:
                - description: 一個症狀與該症出現與否的字串
                - depth: an int. 用於決定問診次數
        """
        # 照格式取出元素
        symptoms = self.parse_input(description)
        depth -= len(symptoms)

        # 初始化疾病成績，清空已存的症狀標記
        self.clear_disease_grade()
        self.clear_symptom_toggle()
        query = ''
        target_sym = ''
        cycle = 0
        cycle_limit = 8

        # 進入診斷迴圈
        while depth != 0 and cycle < cycle_limit:
            choice = 0
            for symptom,flag in symptoms:
                self.evaluate(symptom,flag) # 依症狀出現與否給疾病打分
            cache = sorted(self.diseases_dic.values(), key=lambda disease: disease.grade, reverse=True)

            while choice != "1" and cycle < cycle_limit:
                target_sym, query  = self.get_query(cache,topk=20) # 詢問下一個症狀是否出現
                choice = input(query)
                cycle += 1
            symptoms = [[target_sym,choice]] # 依 choice 更新患者症狀
            depth -= 1

        # 列出診斷結果
        print(self.give_report(cache[:30]))

    def one_pass_diagnose(self, memory, depth=10):
        """依照症狀給予回應或診斷結果。

            Args:
                - memory  : 先前問診的記錄表
                - depth   : 問診次數上限值
        """

        symptoms = parse_input(memory)

        # 初始化疾病成績，清空已存的症狀標記
        self.clear_disease_grade()
        self.clear_symptom_toggle()
        query = ''
        target_sym = ''

        # 進入診斷迴圈
        for symptom,flag in symptoms:
            self.evaluate(symptom,flag) # 依症狀出現與否給疾病打分
        cache = sorted(self.diseases_dic.values(), key=lambda disease: disease.grade, reverse=True)
        target_sym, query  = self.get_query(cache,topk=20) # 詢問下一個症狀是否出現

        if len(memory) >= depth:
            # 回傳診斷結果
            return self.give_report(cache[:30])
        else:
            # 回傳下一個要詢問的症狀
            return query

        print(self.give_report(cache[:30]))

    def give_report(self, topk):

        """
        傳入一個 topk 疾病陣列，回傳該疾病的診斷描述
        """

        candiate = None
        if not self.is_girl: # 濾除婦產科疾病
            for disease in topk:
                if disease.department != '婦產科':
                    candiate = disease
                    break
        else:
            candiate = topk[0]
        #for d in topk:
        #    print(d)


        response_set = [
            "初步判斷可能為%s，" % candiate.name ,"建議前往%s去做更進一步的檢查" % candiate.department,
            "這可能是%s的徵兆，" % candiate.name ,"建議到%s進一步檢查" % candiate.department,
            "目前看起來像是%s，" % candiate.name ,"有需要的話，可以到%s看看" % candiate.department,
            "聽起來感覺像是%s，" % candiate.name ,"可以到%s了解更細部的資訊" % candiate.department
        ]
        report = response_set[random.randrange(0,8,2)] + response_set[random.randrange(1,9,2)]
        return report

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
            #print(disease)
            syms_of_dis = self.get_symptom(disease.name)
            for symptom in syms_of_dis:
                if not self.symptoms_dic[symptom].toggle: #（該症狀是未被詢問過的）
                    symptom_counter[symptom] = (symptom_counter.get(symptom,0)
                                                + 1)

        symptom_counter = sorted(symptom_counter.keys(), key=lambda k:symptom_counter[k], reverse=True)
        #target = symptom_counter[int(len(symptom_counter)/2)] #取出中間值視為最優分割點
        #print(symptom_counter)
        target = symptom_counter[0]
        self.symptoms_dic[target].toggle = True # 標記已被詢問過
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

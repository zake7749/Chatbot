import os
import random
import json

#import diagnose

class MedicalListener(object):

    def __init__(self, console):
        self.console  = console
        self.subject_root     = "主體描述"
        self.description_root = "症狀描述"
        self.symptom_dic = {}
        self.load_symptom_set(path=None)

        self._matchee_index = -1
        self._response = [
            "還有什麼其他症狀嗎？",
            "還有沒有什麼其他症狀呢？",
            "還有什麼不舒服的地方嗎？",
            "還有什麼別的症狀呢？",
            "還有其他地方不舒服的嗎？",
            "還有沒有出現其他症狀？"
        ]

        self.memory = None

    def restore(self, memory):

        """
        依照記憶將任務狀態回復

        Args:
            - memory: 為先前的任務紀錄，儲存已知的症狀
        """

        mem = json.load(memory)
        for key in mem.keys():
            self.symptom_dic[key] = True

    def load_symptom_set(self,path):

        with open(os.path.dirname(__file__) + '/result/symptom_set.txt','r',encoding='utf-8') as input:
            for symptom in input:
                symptom = symptom.strip('\n')
                self.symptom_dic[symptom] = False

    def get_response(self, sentence, domain):

        """
        依據現有的病症資訊，回傳可能疾病或要詢問的症狀
        """

        history = []
        if self.look_up(domain):
        # 判斷是否進入醫生任務

            # 從當前的 sentence 抽取病症信息
            keywords = self.console.word_segment(sentence)
            self.hard_extract(keywords)
            self.reason(keywords)

            # 與先前已知的症狀合併
            for k,v in self.symptom_dic.items():
                if v:
                    history.append(k)

            if len(history) >= 3:
                #進入醫生診斷模組 TODO
                doctor = diagnose.Doctor(False)
                doctor.one_pass_diagnose()
                return [None, "醫生還沒來唷，請稍等一下"]

            else:
                #仍須繼續問診，把目前狀態先回覆給chatbot
                return [json.dumps(history), self._response[random.randrange(0,6)]]
        else:
            return [None, self.console.get_response(domain)]


    def hard_extract(self, keywords):
        """
        透過症狀樹，取得可能的症狀實體
        """
        # 0.88 是為了擋 “尿痛 酸痛”
        print(keywords)
        while True:
            domain = self.rule_match(keywords,reasoning_root="病症",
                                     threshold=0.88, remove=False)
            if domain is not None and not self.symptom_dic[domain]:
                #print(domain)
                if domain != "疼痛":
                    self.symptom_dic[domain] = True
            else:
                break

    def soft_extract(self, keywords):
        """
        透過推理樹，取出對話中可能存在的主體與描述情形。

            Args:
                - sentence: 一句使用者的對話字串
            Return:
                - 一串抽取的症狀列表
        """
        sd_list = []

        while True:
            description_domain = self.rule_match(keywords, self.description_root, threshold=0.4) # 抽取症狀描述
            if description_domain is None:
                break
            subject_domain = self.rule_match(keywords[:self._matchee_index], self.subject_root, threshold=0.4) # 抽取症狀主體
            if subject_domain is None:
                break
            sd_list.append([subject_domain,description_domain])
            #print(description_domain)
            #print(subject_domain)
        return sd_list

    def reason(self, keywords):

        sd_list = self.soft_extract(keywords)

        for subject,description in sd_list:
            result = self.pattern_match(subject,description)
            if result is not None:
                #print("[IN REASONING]: " + result)
                self.symptom_dic[result] = True

    def pattern_match(self, subject, description):

        if subject=="頭部" and description =="痛推理":
            return "頭痛"
        elif subject=="牙齒" and description == "痛推理":
            return "牙痛"
        elif subject=="頭部" and description == "暈推理":
            return "頭暈"
        elif subject=="胃部" and description == "痛推理":
            return "胃痛"
        elif subject=="腹部" and description == "痛推理":
            return "腹痛"
        elif subject=="腹部" and description == "瀉推理":
            return "腹瀉"
        elif subject=="心臟" and description == "痛推理":
            return "心絞痛"
        elif subject=="心臟" and description == "不規則推理":
            return "心律失常"
        elif subject=="腹部" and description == "脹推理":
            return "腹脹"
        elif subject=="胸部" and description == "痛推理":
            return "胸痛"
        elif subject=="胸部" and description == "悶推理":
            return "胸悶"
        elif subject=="臀部" and description == "瘙癢推理":
            return "肛門搔癢"
        elif subject=="腰部" and description == "痛推理":
            return "腰痛"
        elif subject=="嘴巴" and description == "乾推理":
            return "口乾"
        elif subject=="耳朵" and description == "痛推理":
            return "耳痛"
        elif subject=="耳朵" and description == "嗡嗡推理":
            return "耳鳴"
        elif subject=="視力" and description == "模糊推理":
            return "視力模糊"
        elif subject=="鼻子" and description == "出血推理":
            return "鼻出血"
        elif subject=="鼻子" and description == "塞推理":
            return "鼻塞"
        elif subject=="視力" and description == "疲勞推理":
            return "眼疲勞"
        elif subject=="視力" and description == "酸痛推理":
            return "眼疲勞"
        elif subject=="四肢" and description == "酸痛推理":
            return "全身酸痛"
        elif subject=="骨骼" and description == "痛推理":
            return "關節痛"
        elif subject=="胃部" and description == "不適推理":
            return "消化不良"
        elif subject=="胃部" and description == "不舒服推理":
            return "消化不良"
        elif subject=="視力" and description == "酸推理":
            return "眼疲勞"
        elif subject=="四肢" and description == "裂推理":
            return "手足皸裂"
        elif subject=="臀部" and description == "裂推理":
            return "肛裂"
        elif subject=="骨骼" and description == "彎曲推理":
            return "脊柱彎曲"
        elif subject=="全身" and description == "痛推理":
            return "全身酸痛"
        elif subject=="全身" and description == "酸痛推理":
            return "全身酸痛"
        elif subject=="全身" and description == "疲勞推理":
            return "全身酸痛"
        elif subject=="皮膚" and description == "乾推理":
            return "皮膚乾燥"
        elif subject=="尿液" and description == "痛推理":
            return "尿痛"
        elif subject=="大便" and description == "出血推理":
            return "便血"
        elif subject=="尿液" and description == "出血推理":
            return "尿血"
        else:
            return None

    def rule_match(self, keywords, reasoning_root, threshold, remove=True):

        res,path = self.console.rule_match(sentence=keywords, segmented=True,
                                           search_from=reasoning_root, best_only=True)

        if res[0] < threshold: # 已抽取不到任何特徵
            return None
        self._matchee_index = keywords.index(res[2])
        description_domain  = res[1]
        if remove:
            keywords.remove(res[2]) # 刪除已匹配的字串
        return res[1]


    def look_up(self, domain):
        """
        根據抽取出的症狀特徵，決定是進入醫生診斷或是純粹提供建議
        """
        if domain == "扭傷" or domain == "鼻子過敏" or domain == "食物過敏" or domain == "抽筋" or domain == "瘀血":
            return False
        else:
            return True

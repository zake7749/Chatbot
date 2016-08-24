
class MedicalListener(object):

    def __init__(self, console, user_speech):
        self.console  = console
        self.sentence = user_speech
        self.subject_root     = "人體器官"
        self.description_root = "症狀描述"
        self.symptom_dic = {}
        self.load_symptom_set(path=None)

    def load_symptom_set(self,path):

        with open('/medicine/result/symptom_set.txt') as input:
            for symptom in input:
                symptom = symptom.strip('\n')
                self.symptom_dic[symptom] = False

    def hard_extract(self):
        """
        透過症狀樹，取得可能的症狀實體
        """
        pass

    def soft_extract(self):
        """
        透過推理樹，取出對話中可能存在的主體與描述情形。

            Args:
                - sentence: 一句使用者的對話字串
            Return:
                - 一串抽取的症狀列表
        """
        keyword = console.word_segment(self.sentence)
        sd_list = []

        while True:
            description_domain = rule_match(keyword,self.description_root) # 抽取症狀描述
            if description_domain is None:
                break
            subject_root = rule_match(keyword,self.subject_root) # 抽取症狀主體
            if subject_root is None:
                break
            sd_list.append([subject_domain,description_domain])
        return sd_list

    def reason(self, sd_list):

        sd_list = soft_extract()

        for subject,description_root in sd_list:
            result = self.pattern_match(subject,description)
            if result not is None:
                self.symptom_dic[result] = True

    def pattern_match(self, subject, description):

        if subject=="頭部" and description =="痛推理":
            return "頭痛"
        elif subject=="牙齒" and description == "痛推理":
            return "牙痛"
        elif
            pass
        else:
            return None


    def rule_match(self, keyword, reasoning_root):

        res,path = console.rule_match(sentence=keyword, segmented=True,
                            root=self.description_root, best_only=True)
        if res[0] < 0.4: # 已抽取不到任何特徵
            return None
        description_domain  = res[1]
        keyword.remove(res[2]) # 刪除已匹配的字串
        return res[1]

    def decesion(self):
        """
             如果字典中 true 的症狀超過 2 過，進入醫生推理模組，
             否則告訴機器人目前已抽出什麼，
             並要再進一步詢問還有什麼症狀
        """
        pass

    def look_up(domain):
        """
        根據抽取出的症狀特徵，決定是進入醫生診斷或是純粹提供建議
        """
        pass

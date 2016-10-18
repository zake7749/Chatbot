import os
import random
import json

#import diagnose

class HotelListener(object):

    def __init__(self, console):
        self.console  = console
        self.locate_root     = "地點描述"
        self.time_root 		 = "時間描述"
        self.hotel_dic = {}
        self.load_hotel_set(path=None)

        self._matchee_index = -1
        self._response = [
            "還有其他需求嗎？",
            "還有沒有需要其他功能呢？",
            "還有什麼需要的設備嗎？",
            "還有什麼別的要求呢？",
            "還有其他關於房間的需求嗎？",
            "還有沒有其他想要的功能？"
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
            self.hotel_dic[key] = True

    def load_hotel_set(self,path):

        with open(os.path.dirname(__file__) + '/result/hotel_set.txt','r',encoding='utf-8') as input:
            for hotel in input:
                hotel = hotel.strip('\n')
                self.hotel_dic[hotel] = False

    def get_response(self, sentence, domain, target):

        """
        依據現有的病症資訊，回傳可能疾病或要詢問的症狀
        """

        return [None, self._response[random.randrange(0,6)]]


    def hard_extract(self, keywords):
        """
        透過症狀樹，取得可能的症狀實體
        """
        # 0.88 是為了擋 “尿痛 酸痛”
        print(keywords)
        while True:
            domain = self.rule_match(keywords,reasoning_root="住宿",
                                     threshold=0.0, remove=False)
            if domain is not None and not self.hotel_dic[domain]:
                #print(domain)
                if domain != "疼痛":
                    self.hotel_dic[domain] = True
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
            description_domain = self.rule_match(keywords, self.time_root, threshold=0.0) # 抽取症狀描述
            if description_domain is None:
                break
            subject_domain = self.rule_match(keywords[:self._matchee_index], self.locate_root, threshold=0.0) # 抽取症狀主體
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
                self.hotel_dic[result] = True

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
        return True

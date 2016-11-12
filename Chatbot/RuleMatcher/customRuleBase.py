# coding=utf-8
import json
import random

from .rulebase import RuleBase,Rule

class CustomRuleBase(RuleBase):

    """
    用於客製化比對的規則庫，每次比對完即清空規則
    """

    #TODO 客製化的「階段式對話」

    def customMatch(self, sentence, api_key, threshold):

        """
        比對 sentence 與用戶自定義的規則

        Args:
            - sentence : 用戶輸入
            - api_key   : 該名會員的聊天機器人金鑰

        Return: response, 暫時目標 FIXME
            - response : 批配出最適合的主題後，挑選用戶於該主題定義的句子隨機挑一回覆
        """
        # 清空之前讀入的規則
        self.rules.clear()

        # 重新建構規則表
        custom_rules = self.getCustomDomainRules(api_key)
        custom_rules = json.loads(custom_rules)
        self.buildCustomRules(custom_rules)

        # 進行比對
        result_list,path = self.match(sentence, threshold=0.4, root=api_key)

        # 確認最佳回應的有效性
        if result_list[0][0] < threshold:
            return None
            
        # 取出最佳主題的自訂回覆集, 並隨機挑一句回覆
        best_domain = result_list[0][1]
        target_rule = self.rules[best_domain]
        res_num = target_rule.has_response()

        return target_rule.response[random.randrange(0,res_num)]

    def buildCustomRules(self, rules):

        """
        將讀入的規則從字典轉換為 Rule Class 型式

        Args:
            - rules: 由 json.loads 導出的字典型式的規則
        """
        assert self.model is not None, "Please load the model before loading rules."

        for rule in rules:

            domain = rule["domain"]
            concepts_list = rule["concepts"]
            children_list = rule["children"]
            response = rule["response"]

            if domain not in self.rules:
                rule = Rule(domain, concepts_list, children_list, response, self.model)
                self.rules[domain] = rule
            else:
                #TODO Block invalided rule type on front end.
                print("[Rules]: Detect a duplicate domain name '%s'." % domain)

    def getCustomDomainRules(self, key):
        """
        依照 apiKey 取得該用戶的規則集
        """
        #TODO
        #FIXME 採用正規方式驗證

        data = '[{"domain": "TESTING","response": ["這是個測試客製化規則的回覆1","這是個測試客製化規則的回覆2"],"concepts": ["測試"],"children": []}]'

        return data

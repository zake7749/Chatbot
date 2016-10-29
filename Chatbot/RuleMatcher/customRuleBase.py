import json

from .rulebase import RuleBase

class CustomRuleBase(RuleBase):

    """
    用於客製化比對的規則庫，每次比對完即清空規則
    """

    #TODO 客製化的「階段式對話」

    def customMatch(self, sentence, apiKey):

        """
        比對 sentence 與用戶自定義的規則

        Args:
            - sentence : 用戶輸入
            - apiKey   : 該名會員的聊天機器人金鑰
        """
        # 清空之前讀入的規則
        self.rules.clear()

        # 重新建構規則表
        customRules = self.getCustomDomainRules(apiKey)
        customRules = json.loads(customRules)
        self.buildCustomRules(customRules)

        # 進行比對
        return self.match(sentence, threshold=customThreshold, root=apiKey)

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
                if is_root:
                    self.forest_base_roots.append(rule)
            else:
                print("[Rules]: Detect a duplicate domain name '%s'." % domain)

    def getCustomDomainRules(self, key):
        """
        依照 apiKey 取得該用戶的規則集
        """
        #TODO
        return None

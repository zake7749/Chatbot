from ..task import Task
import os
import json
import RuleMatcher.rulebase as rulebase
class PurchaseOperator(Task):

    def __init__(self, console):
        self.console  = console
        self.is_close = False
        self.memory = None
        self.attribute_list = None
        self.current_domain = None
        self.ret = None
        self.rb = rulebase.RuleBase()
        #self.rb.load_model("model/ch-corpus-3sg.bin")
    def get_response(self,user_input, domain, target):
        """
        Return:
            - response : String, 針對使用者的提問給予的答覆
            - status   : List, 若進入某個任務，則回傳目前任務已知的所有屬性
        Args:
            - target   : String, 對照 get_query 的形式，表示當前的user_input是來自
                         bubble button，用來回復該target_attr之狀態
        """
            #依據domain而判斷missing Attribute
            #從句子撈attribute(如果有的話)
            #沒有則問好問滿
        #keywords = self.console.word_segment(user_input)
        self.current_domain = domain
        #res="test"
        #clear demand: return domain
        #hidden demand: ?

        self.ret = domain + "#" + domain
        return [None,self.ret]

    def get_query(self):
        """
        Return:
            - target_attr : String, 預詢問的目標屬性為何
            - candiates  : List, 對該詢問預設的答案列表 (bubble buttons)
        """
        pass
    def restore(self, memory):
        """
        Args:
            - memory: 為一 json 形式的字典，
            來自之前由 get_response 送出的 status，依各 module 自行實作狀態回復方法
        """

    def get_suggest(self):
        pass
    def debug(self):

        pass
    def load_attribute(self,path):
        with open (os.path.dirname(__file__) + '/purchase_attr.json','r') as data:
            self.attribute_list = json.load(data)


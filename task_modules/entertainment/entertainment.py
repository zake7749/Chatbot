class entertainment(object):

    def __init__(self, console):
        self.console  = console
        self.console  = console
        self.currrent_domain = None
		
    def get_response(self,user_input, domain, target):
        """
        Return:
            - response : String, 針對使用者的提問給予的答覆
            - status   : List, 若進入某個任務，則回傳目前任務已知的所有屬性，否則為 None
        Args:
            - target   : String, 對照 get_query 的形式，表示當前的user_input是來自
                         bubble button，用來回復該target_attr之狀態
        """
		#need 未知>分類>地點.專名>回傳
        keywords = self.console.word_segment(user_input) #cut sentence ,return list
        if "訂" in user_input:
            res_url = "https://tw.eztable.com/search?q=" + domain
            self.currrent_domain = res_url
            return [None , res_url]
        else :
            self.currrent_domain = domain
            return [None , domain]
		
	
    def get_query(self):
        """
        Return:
        - target_attr : String, 預詢問的目標屬性為何
        - candiaties  : List, 對該詢問預設的答案列表 (bubble buttons)
        """
        return [None, self.currrent_domain]
    def restore(self, memory):
        pass
    def get_suggest(self):
        pass
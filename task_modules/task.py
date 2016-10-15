class Task(object):

    """
        任務模組的統一接口定義
    """
    def __init__(self, console):
        self.console  = console
        self.is_close = False

    def get_response(self,user_input, domain, target):
        """
        Return:
            - response : String, 針對使用者的提問給予的答覆
            - status   : List, 若進入某個任務，則回傳目前任務已知的所有屬性，否則為 None
        Args:
            - target   : String, 對照 get_query 的形式，表示當前的user_input是來自
                         bubble button，用來回復該target_attr之狀態
        """

        raise NotImplementedError

    def get_query(self):
        """
        Return:
            - target_attr : String, 預詢問的目標屬性為何，若不存在則為 None
            - candiaties  : List, 對該詢問預設的答案列表 (bubble buttons)，若不存在則為 None
        """
        raise NotImplementedError

    def restore(self, memory):
        """
        Args:
            - memory: 為一 json 形式的字典，
            來自之前由 get_response 送出的 status，依各 module 自行實作狀態回復方法
        """
        raise NotImplementedError

    def get_suggest(self):
        """
        Return:
            - place: 當一個指標任務結束時，依用戶需求推薦地點集名稱或絕對位置，若任務尚未結束則為 None
        """
        raise NotImplementedError

    def debug(self):

        pass

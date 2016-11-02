from responsesEvaluate import Evaluator

import match

import json
import os
import random
import logging

def main():

    chatter = GossipBot()
    #chatter.randomTalks()
    chatter.chatTime()


class GossipBot(object):

    """
    八卦板聊天機器人 ob'_'ov
    """
    def __init__(self):
        self.matcher = match.getMatcher("Fuzzy")
        self.evaluator = Evaluator()
        self.testSegment()
        self.defaultResponse = [
            "你在說什麼呢？",
            "我不太明白你的意思"
        ]

    def testSegment(self):
        logging.info("測試斷詞模塊中")
        try:
            self.matcher.wordSegmentation("測試一下斷詞")
            logging.info("測試成功")
        except Exception as e:
            logging.info(repr(e))
            logging.info("模塊載入失敗，請確認data與字典齊全")

    def chatTime(self):
        print("MianBot: 您好，我是你的老朋友眠寶，讓我們來聊聊八卦吧 o_o ")
        while True:
            query = input("User: ")
            print("MianBot: " +self.getResponse(query))

    def getResponse(self,query,threshold=50):

        title,index = self.matcher.match(query)
        sim = self.matcher.getSimilarity()
        if sim < threshold:
            return self.defaultResponse[random.randrange(0,len(self.defaultResponse))]
        else:
            res = json.load(open(os.path.join("data/processed/reply/",str(int(index/1000))+'.json'),'r',encoding='utf-8'))
            targetId = index % 1000
            candiates = self.evaluator.getBestResponse(res[targetId],topk=3)
            reply = self.randomPick(candiates)
            return reply

    def randomPick(self, answers):
        return answers[random.randrange(0,len(answers))][0]

    def randomTalks(self, num=100):
        with open("data/Titles.txt",'r',encoding='utf-8') as data:
            titles = [line.strip('\n') for line in data]
        for i in range(0,num):
            query = titles[random.randrange(0,len(titles))]
            print("User: " + query)
            print("MianBot: " +self.getResponse(query))

if __name__=="__main__":
    main()

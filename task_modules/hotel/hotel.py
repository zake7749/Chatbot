import os
import random
import json
import datetime
import requests
from bs4 import BeautifulSoup
#import diagnose

class HotelListener(object):

	def __init__(self, console):
		self.console  = console
		self.locate	 = ""
		self.month 		 = ""
		self.add_day 		 = ""
		self.week 		 = ""
		self.day		 = ""
		self.date 		 = ""
		self.end 		 = ""
		self.fac		 = []
		self.hotel_dic = {"locate":None,
							"time":None,
							"end":None}

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

	def get_query(self):
		"""
		僅適用於醫生模式，傳回欲問診的病症與預設答案表列
		"""
		return None,None
	def debug(self,log=None):
		pass
		
	def get_response(self, sentence, domain, target):

		"""
		依據現有的病症資訊，回傳可能疾病或要詢問的症狀
		"""
		if self.look_up(domain):
			keywords = self.console.word_segment(sentence)
			self.time_extract(keywords)
			self.locate_extract(keywords)
			if self.hotel_dic["time"] is not None and self.hotel_dic["locate"] is not None:
				result_num = 0
				result = []
				res = requests.get("https://www.agoda.com/zh-tw/pages/agoda/default/DestinationSearchResult.aspx?city="
					+ self.hotel_dic["locate"] + "&checkIn=" + self.hotel_dic["time"] + "&checkOut=" + self.hotel_dic["end"] + "&children=0&isFromSearchBox=true&adults=6&rooms=6")
				soup = BeautifulSoup(res.text)
				for a in soup.findAll("img", { "data-selenium": "hotel-img"}):
					if a['alt'].encode('big5','ignore').decode('big5') not in result:
						result.append(a['alt'].encode('big5','ignore').decode('big5'))
						result_num += 1
					if result_num == 5:
						break
				if len(result) == 0:
					return [None, "不好意思，目前沒有適合的飯店"]
				else:	
					return [None, "#".join(result)]
			else:
				return [json.dumps(self.hotel_dic), self._response[random.randrange(0,6)] + self.date]
		else:
			return [None, self._response[random.randrange(0,6)]]

	def locate_extract(self, keywords):
		
		for key in keywords:
			k = self.rule_match(keywords,reasoning_root="住宿",threshold=0.0, remove=False)
			if k is not None:
				print("[DEBUG]: hard_extract " + k + " " + key)
			if key == '台北市' or key == '台北' or key == '新北市' or key == '新北':
				self.locate	 = "4951"
			if key == '基隆市' or key == '基隆':
				self.locate	 = "17048"
			if key == '桃園市' or key == '桃園':
				self.locate	 = "8453"
			if key == '新竹縣' or key == '新竹':
				self.locate	 = "12711"
			if key == '苗栗縣' or key == '苗栗':
				self.locate	 = "287008"
			if key == '台中市' or key == '台中':
				self.locate	 = "12080"
			if key == '彰化縣' or key == '彰化':
				self.locate	 = "18341"
			if key == '南投縣' or key == '南投':
				self.locate	 = "18346"
			if key == '雲林縣' or key == '雲林':
				self.locate	 = "18352"
			if key == '嘉義縣' or key == '嘉義':
				self.locate	 = "11977"
			if key == '台南市' or key == '台南':
				self.locate	 = "18347"
			if key == '高雄市' or key == '高雄':
				self.locate	 = "756"
			if key == '屏東縣' or key == '屏東':
				self.locate	 = "11459"
			if key == '宜蘭縣' or key == '宜蘭':
				self.locate	 = "88773"
			if key == '花蓮縣' or key == '花蓮':
				self.locate	 = "23127"
			if key == '台東縣' or key == '台東':
				self.locate	 = "4740"
			if key == '澎湖縣' or key == '澎湖':
				self.locate	 = "106001"
			if key == '金門縣' or key == '金門':
				self.locate	 = "286060"
			if key == '馬祖列島' or key == '馬祖' or key == '連江縣':
				self.locate	 = "702190"
			if key == '墾丁':
				self.locate	 = "18343"
			if self.locate is not "":
				self.hotel_dic["locate"] = self.locate

	def time_extract(self, keywords):
		while True:
			target_week = 0
			target_month = 0
			target_day = 0
			for key in keywords:
				if key == '一月' or key == '1月':
					self.month = '一月' 
					target_month = 1
				elif key == '二月' or key == '2月':
					self.month = '二月' 
					target_month = 2
				elif key == '三月' or key == '3月':
					self.month = '三月'
					target_month = 3
				elif key == '四月' or key == '4月':
					self.month = '四月' 
					target_month = 4
				elif key == '五月' or key == '5月':
					self.month = '五月' 
					target_month = 5
				elif key == '六月' or key == '6月':
					self.month = '六月'
					target_month = 6
				elif key == '七月' or key == '7月':
					self.month = '七月' 
					target_month = 7
				elif key == '八月' or key == '8月':
					self.month = '八月' 
					target_month = 8
				elif key == '九月' or key == '9月':
					self.month = '九月' 
					target_month = 9
				elif key == '十月' or key == '10月':
					self.month = '十月' 
					target_month = 10
				elif key == '十一月' or key == '11月':
					self.month = '十一月' 
					target_month = 11
				elif key == '十二月' or key == '12月':
					self.month = '十二月'
					target_month = 12
				elif key == '一日' or key == '一號':
					self.day = '一日'
					target_day = 1
				elif key == '二日' or key == '二號':
					self.day = '二日'
					target_day = 2
				elif key == '三日' or key == '三號':
					self.day = '三日'
					target_day = 3
				elif key == '四日' or key == '四號':
					self.day = '四日'
					target_day = 4	
				elif key == '五日' or key == '五號':
					self.day = '五日'
					target_day = 5
				elif key == '六日' or key == '六號':
					self.day = '六日'
					target_day = 6
				elif key == '七日' or key == '七號':
					self.month = '七日'
					target_day = 7
				elif key == '八日' or key == '八號':
					self.month = '八日'
					target_day = 8
				elif key == '九日' or key == '九號':
					self.month = '九日'
					target_day = 9
				elif key == '十日' or key == '十號':
					self.month = '十日'
					target_day = 10
				elif key == '十一日' or key == '十一號':
					self.month = '十一日'
					target_day = 11
				elif key == '十二日' or key == '十二號':
					self.month = '十二日'
					target_day = 12
				elif key == '十三日' or key == '十三號':
					self.month = '十三日'
					target_day = 13
				elif key == '十四日' or key == '十四號':
					self.month = '十四日'
					target_day = 14
				elif key == '十五日' or key == '十五號':
					self.month = '十五日'
					target_day = 15
				elif key == '十六日' or key == '十六號':
					self.day = '十六日'
					target_day = 16
				elif key == '十七日' or key == '十七號':
					self.day = '十七日'
					target_day = 17
				elif key == '十八日' or key == '十八號':
					self.day = '十八日'
					target_day = 18
				elif key == '十九日' or key == '十九號':
					self.month = '十九日'
					target_day = 19
				elif key == '二十日' or key == '二十號':
					self.day = '二十日'
					target_day = 20
				elif key == '二十一日' or key == '二十一號':
					self.day = '二十一日'
					target_day = 21
				elif key == '二十二日' or key == '二十二號':
					self.day = '二十二日'
					target_day = 22
				elif key == '二十三日' or key == '二十三號':
					self.day = '二十三日'
					target_day = 23
				elif key == '二十四日' or key == '二十四號':
					self.day = '二十四日'
					target_day = 24
				elif key == '二十五日' or key == '二十五號':
					self.day = '二十五日'
					target_day = 25
				elif key == '二十六日' or key == '二十六號':
					self.day = '二十六日'
					target_day = 26
				elif key == '二十七日' or key == '二十七號':
					self.day = '二十七日'
					target_day = 27
				elif key == '二十八日' or key == '二十八號':
					self.day = '二十八日'
					target_day = 28
				elif key == '二十九日' or key == '二十九號':
					self.day = '二十九日'
					target_day = 29
				elif key == '三十日' or key == '三十號':
					self.day = '三十日'
					target_day = 30
				elif key == '三十一日' or key == '三十一號':
					self.day = '三十一日'
					target_day = 31
				elif key == '星期一' or key == '禮拜一':
					self.week = '星期一'
					target_week = 0
				elif key == '星期二' or key == '禮拜二':
					self.week = '星期二' 
					target_week = 1
				elif key == '星期三' or key == '禮拜三':
					self.week = '星期三' 
					target_week = 2
				elif key == '星期四' or key == '禮拜四':
					self.week = '星期四' 
					target_week = 3
				elif key == '星期五' or key == '禮拜五':
					self.week = '星期五' 
					target_week = 4
				elif key == '星期六' or key == '禮拜六':
					self.week = '星期六' 
					target_week = 5
				elif key == '星期日' or key == '禮拜日' or key == '星期天' or key == '星期日':
					self.week = '星期日'
					target_week = 6
				elif key == '明天':
					self.add_day = '明天' 
				elif key == '後天':
					self.add_day = '後天'
				
			now = datetime.datetime.now()
				
			if self.add_day is not "":
				self.hotel_dic["time"] = 1
				if self.add_day == '明天':
					now += datetime.timedelta(days=1)
					self.date = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
					now += datetime.timedelta(days=1)
					self.end = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
				elif self.add_day == '後天':
					now += datetime.timedelta(days=2)
					self.date = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
					now += datetime.timedelta(days=1)
					self.end = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
				self.hotel_dic["time"] = self.date
				self.hotel_dic["end"] = self.end
					
			elif self.month is not "" and self.day is not "":
				if now < datetime.datetime(now.year, target_month, target_day):
					if target_month == 4 or target_month == 6 or target_month == 9 or target_month == 11:
						if target_day > 30:
							self.date = "ERROR!! Invaild Day!!"
							return
					if target_month == 2:
						if now.year % 4000 == 0:
							if target_day > 28:
								self.date = "ERROR!! Invaild Day!!"
								return
						elif now.year % 400 == 0:
							if target_day > 29:
								self.date = "ERROR!! Invaild Day!!"
								return
						elif now.year % 100 == 0:
							if target_day > 28:
								self.date = "ERROR!! Invaild Day!!"
								return
						elif now.year % 4 == 0:
							if target_day > 29:
								self.date = "ERROR!! Invaild Day!!"
								return
					now = datetime.date(now.year, target_month, target_day)
					self.date = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
					now += datetime.timedelta(days=1)
					self.end = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
				else:
					if target_month == 4 or target_month == 6 or target_month == 9 or target_month == 11:
						if target_day > 30:
							self.date = "ERROR!! Invaild Day!!"
							return
					if target_month == 2:
						if (now.year + 1) % 4000 == 0:
							if target_day > 28:
								self.date = "ERROR!! Invaild Day!!"
								return
						elif (now.year + 1) % 400 == 0:
							if target_day > 29:
								self.date = "ERROR!! Invaild Day!!"
								return
						elif (now.year + 1) % 100 == 0:
							if target_day > 28:
								self.date = "ERROR!! Invaild Day!!"
								return
						elif (now.year + 1) % 4 == 0:
							if target_day > 29:
								self.date = "ERROR!! Invaild Day!!"
								return
					now = datetime.date(now.year + 1, target_month, target_day)
					self.date = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
					now += datetime.timedelta(days=1)
					self.end = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
				self.hotel_dic["time"] = self.date
				self.hotel_dic["end"] = self.end
				
			elif self.month is "" and self.day is not "":
				if now.day() < target_day:
					if now.month() == 4 or now.month() == 6 or now.month() == 9 or now.month() == 11:
						if target_day > 30:
							self.date = "ERROR!! Invaild Day!!"
							return
					if now.month() == 2:
						if now.year % 4000 == 0:
							if target_day > 28:
								self.date = "ERROR!! Invaild Day!!"
								return
						elif now.year % 400 == 0:
							if target_day > 29:
								self.date = "ERROR!! Invaild Day!!"
								return
						elif now.year % 100 == 0:
							if target_day > 28:
								self.date = "ERROR!! Invaild Day!!"
								return
						elif now.year % 4 == 0:
							if target_day > 29:
								self.date = "ERROR!! Invaild Day!!"
								return
					now = datetime.date(now.year, now.month, target_day)
					self.date = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
					now += datetime.timedelta(days=1)
					self.end = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
				else:
					if now.day() < target_day:
						if now.month() == 3 or now.month() == 5 or now.month() == 7 or now.month() == 10:
							if target_day > 30:
									self.date = "ERROR!! Invaild Day!!"
									return
						if now.month() == 1:
							if now.year % 4000 == 0:
								if target_day > 28:
									self.date = "ERROR!! Invaild Day!!"
									return
							elif now.year % 400 == 0:
								if target_day > 29:
									self.date = "ERROR!! Invaild Day!!"
									return
							elif now.year % 100 == 0:
								if target_day > 28:
									self.date = "ERROR!! Invaild Day!!"
									return
							elif now.year % 4 == 0:
								if target_day > 29:
									self.date = "ERROR!! Invaild Day!!"
									return
					now = datetime.date(now.year, now.month + 1, target_day)
					self.date = str(now.year) + "-" + str(now.month + 1) + "-" + str(target_day)
					now += datetime.timedelta(days=1)
					self.end = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
				self.hotel_dic["time"] = self.date
				self.hotel_dic["end"] = self.end
				
			elif self.week is not "":
				if now.weekday() < target_week:
					now += datetime.timedelta(days=target_week - now.weekday())
					self.date = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
					now += datetime.timedelta(days=1)
					self.end = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
				else:
					now += datetime.timedelta(days=7 - target_week + now.weekday())
					self.date = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
					now += datetime.timedelta(days=1)
					self.end = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
				self.hotel_dic["time"] = self.date
				self.hotel_dic["end"] = self.end
			break
				

	def rule_match(self, keywords, reasoning_root, threshold, remove=True):

		res,path = self.console.rule_match(sentence=keywords, segmented=True,
										   search_from=reasoning_root, best_only=True)

		if res[0] < threshold: # 已抽取不到任何特徵
			return None
		self._matchee_index = keywords.index(res[2])
		locate_domain  = res[1]
		if remove:
			keywords.remove(res[2]) # 刪除已匹配的字串
		return res[1]


	def look_up(self, domain):
		"""
		根據抽取出的症狀特徵，決定是進入醫生診斷或是純粹提供建議
		"""
		if domain == "查詢":
			return False
		else:
			return True

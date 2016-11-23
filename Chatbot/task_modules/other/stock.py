import sys
import time
import requests
import csv
import os
import re
class Stock(object):

	def __init__(self, console):
		self.console  = console
		self.is_close = False
    
	def get_response(self,user_input, domain, target):
		"""
		Return:
			- response : String, 針對使用者的提問給予的答覆
			- status   : List, 若進入某個任務，則回傳目前任務已知的所有屬性
		Args:
			- target   : String, 對照 get_query 的形式，表示當前的user_input是來自
						 bubble button，用來回復該target_attr之狀態
		"""
		#print("enter stock")
		output = ""
		stock_name = ""
		stock_no = 'None'
		keywords = self.console.word_segment(user_input)
		#print(keywords)
		for nm in keywords:
			#print("股")
			stock_no = self.get_stock_no(nm)
			if 	stock_no is not 'None':
				#print(stock_no)
				break
		if stock_no == 'None':
			output = "找不到關於該股票的資料"
			#print("no data\n")
			return [None,output]
		#stock_no = "tse_2357.tw"
		req = requests.session()
		req.get('http://mis.twse.com.tw/stock/index.jsp',headers = {'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'})
		timestamp = int(time.time()*1000+1000000)
		response = req.get('http://mis.twse.com.tw/stock/api/getStockInfo.jsp?_={}&ex_ch={}'.format(timestamp,stock_no))
		res_json = response.json()
		#print(res_json)
		msgArray = res_json['msgArray']
		
		for key in msgArray:
			name = key['n']
			no = key['c']
			open_price = float(key['o'])
			price = float(key['z'])
			diff = round(price - open_price, 2)
			highest = key['h']
			lowest = key['l']
			number = key['v']
		
		output = '股票名稱:' + name + '\n' +'股票代碼:' + no + '\n' +'開盤價格:' + str(open_price) + '\n' +'該盤成交價格:' + str(price) + '\n' +'漲跌價:' + str(diff) + '\n' +'最高價:' + highest + '\n' +'最低價:' + lowest + '\n' +'張數:' + number + '\n'
		#print(msgArray)
		return [None,output]
	
	def get_stock_no(self, stock_name):
		file = open(os.path.dirname(__file__)+ '/data.csv','r') #定期在收盤前更新csv
		next(file)
		next(file)
		#csv_read = csv.DictReader(file)
		
		stock_url = 'None'
		for col in file.readlines():
			m = re.search('([0-9]{4}[ ]{2}|[0-9]{5}[ LRU]{1}|[0-9]6),([^ ]*)( *),',col)
			if m:
				print(m.group(2))
				print(stock_name)
				if stock_name == m.group(2):
					stock_no = m.group(1)
					stock_url = 'tse_'+str(stock_no).strip()+'.tw'
		file.close()
			
		return stock_url
	def get_query(self):
		pass
	def restore(self,memory):
		pass
	def get_suggest(self):
		pass
	def debug(self):
		pass
	

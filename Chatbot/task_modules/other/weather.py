# -*- coding: utf-8 -*-

import sys
import urllib.request
import string
import xml.etree.ElementTree as ET


class Weather(object):

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
		xml_path = ""
		output = ""
		keyword = self.console.word_segment(user_input) #return a list
		#weather_locate = user_input
		#domain = 天氣??		
		
		if "台北" in keyword :
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_01.xml"
		elif "高雄" in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_02.xml"
		elif "基隆" in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_03.xml"
		elif "新北"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_04.xml"
		elif "桃園"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_05.xml"
		elif "新竹"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_06.xml"
		elif "苗栗"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_07.xml"
		elif "台中"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_08.xml"
		elif "彰化"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_09.xml"
		elif "南投"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_10.xml"
		elif "雲林"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_11.xml"
		elif "嘉義"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_12.xml"
		elif "台南"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_13.xml"
		elif "屏東"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_15.xml"
		elif "宜蘭"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_17.xml"
		elif "花蓮"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_18.xml"
		elif "台東"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_19.xml"
		elif "澎湖"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_20.xml"
		elif "金門"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_21.xml"
		elif "連江"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_22.xml"
		elif "馬祖"  in keyword:
			xml_path = "http://www.cwb.gov.tw/rss/forecast/36_22.xml"
		else :
			output = "找不到關於該縣(市)的資料"
			return [None,output]

		weather_file = urllib.request.urlopen(xml_path)
		read_file = weather_file.read().decode('utf-8')
		tree = ET.fromstring(read_file)	
		weather_file.close()
		if "今天" in keyword:
			root = tree.iterfind('channel/item/title')
			for day in root:
				output = day.text
				break
		elif "明天" in keyword:
			root = tree.iterfind('channel/item/description')
			for next in root:
				output = next.text
				break
		#需要更精確判斷		
		elif "下週" in keyword: 
			root = tree.iterfind('channel/item/description')
			for next in root:
				break
			for next in root:
				output = next.text.replace('<BR>','').replace('\t','')
				break
		else :
			output = "out of range"
		
		return [None,output]
#coding=utf-8
#author: Justin Yang

import requests
from bs4 import BeautifulSoup
import lxml
import time
import sys
import os

def main():
	symptomSet = loadDataWithSet("symptoms.txt")
	# result = matchDiseaseWithSymptoms(symptomSet, "rawpage")
	result = getDCPair("data")
	writeDDPair2file('result/dcpair',result)
	# writeDSPairs2file('result/without_suffix_6', result)

def loadDataWithSet(path):

	elementSet = set()
	with open(path, 'r') as file:
		for line in file:
			element = line.strip('\n')
			elementSet.add(element)
	return elementSet

def matchDiseaseWithSymptoms(sym,dir):

	'''從原始頁面中抽取疾病與症狀的配對集
	'''
	dic = {}

	for filename in os.listdir("./"+dir):
		# IGNORE .DS_STORE
		if not filename.startswith('.'):
			soup = BeautifulSoup(open(dir+"/"+filename),"lxml")

			# clean the url in 症状查詢專題 like http://cht.a-hospital.com/w/%E6%96%9C%E8%A7%86
			for nonce in soup.find_all('table'):
				nonce.clear()
			for candidate in soup.select("p > a"):
				if candidate.text in sym:
					#d_xxx.txt
					disease_mata = filename.split(".")[0]
					disease = disease_mata.split("_")[1]
					if candidate.text in dic:
						dic[candidate.text].add(disease)
					else:
						dic[candidate.text] = set()
						dic[candidate.text].add(disease)
	return dic

def getDCPair(dir):

	'''取得疾病的對應科別，資料來自data，格式為:'symptom:disease1,disease2......'
	'''

	dic = {}
	for department in os.listdir("./"+dir):
		# IGNORE .DS_STORE
		if not department.startswith('.'):
			with open(dir+"/"+department) as input:
				diseaseSet = set()
				for line in input:
					line = line.strip('\n')
					line = line.strip(',')
					diseaseList = line.split(':')[1].split(',')
					for disease in diseaseList:
						if disease not in diseaseSet:
							diseaseSet.add(disease)
				dic[department.split('.')[0]] = diseaseSet
	return dic

def writeDSPairs2file(filename,dic):

	'''輸出症狀集，急性XXX與慢性XXX統一視為XXX
	'''
	with open(filename,'w',encoding='utf-8') as res:
		for symptom,diseaseSet in dic.items():
			res.write(symptom+":")
			for disease in diseaseSet:
				if disease != symptom and disease != "口臭":
					if "急性" not in disease and "慢性" not in disease:
						res.write(disease+",")
			res.write('\n')

def writeDDPair2file(filename,dic):

	'''輸出疾病與部門的配對列表
	'''
	with open(filename,'w',encoding='utf-8') as output:
		for department,diseaseSet in dic.items():
			output.write(department+":")
			for disease in diseaseSet:
				output.write(disease+",")
			output.write('\n')

if __name__=="__main__":
	main()

# -*- coding: utf-8 -*-

from gensim.models import word2vec
from gensim import models
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
model = models.Word2Vec.load_word2vec_format('model/ch-corpus.bin',binary=True)

while True:
	try:
		query = input('Query:')
		q_list = query.split()

		if q_list[-1] == "2":
			print("詞相似度")
			y1 = model.similarity(q_list[0],q_list[1])
			print(y1)
		elif q_list[-1] == "1":
			print("同義詞排序")
			y2 = model.most_similar(q_list[0],topn = 100)
			for item in y2:
				print(item[0]+","+str(item[1]))
		else:
			print("推理")
			y3 = model.most_similar([q_list[0],q_list[1]], [q_list[2]], topn= 100)
			for item in y3:
				print(item[0]+","+str(item[1]))
		print("----------------------------")
	except Exception as e:
		print(repr(e))
		pass
if __name__ == "__main__":
    pass
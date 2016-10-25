from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from trips.models import Post
from trips.models import Article
import os
import json
import subprocess, sys
from django import forms
import chatbot
import random
#from ..mysite import mysite
import re
# -*- coding: utf8 -*-

class ArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ['frontId', 'content' ]

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['iden', 'content','domain']

def creates(request):
	if request.method == 'POST':
		form = ArticleForm(request.POST)
		if form.is_valid():
			new_article = form.save()
			Post.objects.create(iden=new_article.title,content=new_article.content)
			return HttpResponseRedirect('/index/'+new_article.title)

	form = ArticleForm()
	return render(request, 'create_article.html', {'form': form})

def index(request):
	global output
	if request.method == 'POST':
		form = ArticleForm(request.POST)
		new_article = form.save()
		if form.is_valid():
			if new_article.frontId == '':
				while(1):
					myid = random.randint(0,99)
					post = Post.objects.filter(iden=myid)
					if len(post) == 0:
						break
					#print(output[1])
				output = chatb.listen(new_article.content)
				#output0 = output[0].decode('utf8')
				
				if output[1] is not None:
					Post.objects.create(iden=myid,content=output[1],domain = chatb.root_domain)
					return HttpResponse(json.dumps({'ID':str(myid),'reply':output[0]}))
					#return render(request, 'get.html', {'form': form,'data': str(myid)+"#"+output[0]})
				#print(str(myid)+'#'+output[0])
				else:
					return HttpResponse(json.dumps({'reply':output[0]}))
					#return render(request, 'get.html', {'form': form,'data': output[0]})
			else:
				post = Post.objects.filter(iden=new_article.frontId)
				if len(post) == 0:
					print('your Id have ERROR!!')
					return HttpResponse(json.dumps({'reply':'your Id have ERROR!!'}))
					#return render(request, 'get.html', {'form': form,'data': 'your Id have ERROR!!'})
				else:
					data = Post.objects.get(iden=new_article.frontId).content
					chatb.root_domain = Post.objects.get(iden=new_article.frontId).domain
					output = chatb.listen(new_article.content)
					temp = list(output[1])
					for i in range(0, len(temp), 1):
						if temp[i] != data[i]:
							if temp[i] == 't' and data[i] == 'n':
								data[i] = temp[i]
							if temp[i] == 'r' and data[i] == 'u':
								data[i] = temp[i]
							if temp[i] == 'u' and data[i] == 'l':
								data[i] = temp[i]
							if temp[i] == 'e' and data[i] == 'l':
								data[i] = temp[i]
					print("".join(data))
					print(len(temp))
					if output[1] is not None:
						Post.objects.filter(iden=new_article.frontId).update(content="".join(data))
						return HttpResponse(json.dumps({'ID':new_article.frontId,'reply':output[0]}))
						#return render(request, 'get.html', {'form': form,'data': new_article.frontId+'#'+output[0]})
					else:
						Post.objects.get(iden=new_article.frontId).delete()
						return HttpResponse(json.dumps({'ID':new_article.frontId,'reply':output[0]}))
						#return render(request, 'get.html', {'form': form,'data': output[0]})
					#print(Post.objects.get(iden=new_article.frontId).content.split('#'))
					
		#	process.stdin.write(str.encode(new_article.content))
		#	stdo = process.communicate(input=(new_article.content).encode())[0]
		#	print(process.stdout.readline())
		#	process.stdout.close()

	form = ArticleForm()
	global chatb
	chatb = chatbot.Chatbot()
	
	#process = Popen('python C:/Users/aa/proj_DB/mysite/Chatbot-master/chatbot.py', stdin=PIPE)
	#for line in iter(process.stdout.readline,''):
	#	print("test:", line.rstrip())
	#	if line.rstrip() == b'[Console] Initialized successfully :>':
	#		print("I am break")
	#		break
	#subprocess.Popen('python C:/Users/aa/proj_DB/mysite/Chatbot-master/chatbot.py', stdin=PIPE, stderr=STDOUT,executable=None, shell=False)
	return render(request, 'create_article.html', {'form': form})


def request_data(request):
	if request.method == 'POST':
		form = ArticleForm(request.POST)
		if form.is_valid():
			new_article = form.save()
	#		print(process.stdout.readline())
	#		process.stdout.close()
			return render(request, 'get.html', {'form': form,'data': new_article.content})

	form = ArticleForm()
	#subprocess.Popen('python C:/Users/aa/proj_DB/mysite/Chatbot-master/chatbot.py', stdin=PIPE, stderr=STDOUT,executable=None, shell=False)
	return render(request, 'get.html', {'form': form})
	
def submit(request, pk, data):
	print(pk)
	print(data)
	post = Post.objects.filter(iden=pk)
	if len(post) == 0:
		Post.objects.create(iden=pk,content=data)
	return render(request, 'submit.html', {'post': pk,'data': data})
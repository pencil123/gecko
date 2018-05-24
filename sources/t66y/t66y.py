#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import sys
import json
import time
import types
from bs4 import BeautifulSoup as BS

from guess import Guess
from libs.wget import wget
from libs.mysqlconn import MysqlConn
from image_page import image_page

class t66y(object):
	def __init__(self):
		self.t66y_config = {}
		self.t66y_config['domain'] = 'https://t66y.com/'
		self.t66y_config['forum_next_text']='下一頁'
		self.wget = wget()
		self.db =MysqlConn()
	def run(self):
		#handler = Guess()
		self.op_index()
		#print self.wget.get_content(self.domain)

	def op_index(self):
		forum_list =[
		{'id':1,'forum_url':'https://t66y.com/thread0806.php?fid=1','forum_type':'images'},
		{'id':2,'forum_url':'https://t66y.com/thread0806.php?fid=2','forum_type':'images'},
		{'id':4,'forum_url':'https://t66y.com/thread0806.php?fid=4','forum_type':'images'},
		{'id':53,'forum_url':'https://t66y.com/thread0806.php?fid=5&type=3','forum_type':'images'},
		{'id':52,'forum_url':'https://t66y.com/thread0806.php?fid=5&type=2','forum_type':'images'},
		{'id':51,'forum_url':'https://t66y.com/thread0806.php?fid=5&type=1','forum_type':'images'},
		{'id':6,'forum_url':'https://t66y.com/thread0806.php?fid=6','forum_type':'images'},
		{'id':7,'forum_url':'https://t66y.com/thread0806.php?fid=7','forum_type':'images'},
		{'id':812,'forum_url':'https://t66y.com/thread0806.php?fid=8&type=12','forum_type':'images'},
		{'id':84,'forum_url':'https://t66y.com/thread0806.php?fid=8&type=4','forum_type':'images'},
		{'id':83,'forum_url':'https://t66y.com/thread0806.php?fid=8&type=3','forum_type':'images'},
		{'id':82,'forum_url':'https://t66y.com/thread0806.php?fid=8&type=2','forum_type':'images'},
		{'id':81,'forum_url':'https://t66y.com/thread0806.php?fid=8&type=1','forum_type':'images'},
		{'id':10,'forum_url':'https://t66y.com/thread0806.php?fid=10','forum_type':'images'},
		{'id':11,'forum_url':'https://t66y.com/thread0806.php?fid=11','forum_type':'images'},
		{'id':12,'forum_url':'https://t66y.com/thread0806.php?fid=12','forum_type':'images'},
		{'id':13,'forum_url':'https://t66y.com/thread0806.php?fid=13','forum_type':'images'},
		{'id':14,'forum_url':'https://t66y.com/thread0806.php?fid=14','forum_type':'images'},
		{'id':15,'forum_url':'https://t66y.com/thread0806.php?fid=15','forum_type':'images'},
		{'id':16,'forum_url':'https://t66y.com/thread0806.php?fid=16','forum_type':'images'},
		{'id':20,'forum_url':'https://t66y.com/thread0806.php?fid=20','forum_type':'images'},
		{'id':215,'forum_url':'https://t66y.com/thread0806.php?fid=21&type=5','forum_type':'images'},
		{'id':214,'forum_url':'https://t66y.com/thread0806.php?fid=21&type=4','forum_type':'images'},
		{'id':213,'forum_url':'https://t66y.com/thread0806.php?fid=21&type=3','forum_type':'images'},
		{'id':212,'forum_url':'https://t66y.com/thread0806.php?fid=21&type=2','forum_type':'images'},
		{'id':211,'forum_url':'https://t66y.com/thread0806.php?fid=21&type=1','forum_type':'images'},
		{'id':226,'forum_url':'https://t66y.com/thread0806.php?fid=22&type=6','forum_type':'images'},
		{'id':225,'forum_url':'https://t66y.com/thread0806.php?fid=22&type=5','forum_type':'images'},
		{'id':224,'forum_url':'https://t66y.com/thread0806.php?fid=22&type=4','forum_type':'images'},
		{'id':223,'forum_url':'https://t66y.com/thread0806.php?fid=22&type=3','forum_type':'images'},
		{'id':222,'forum_url':'https://t66y.com/thread0806.php?fid=22&type=2','forum_type':'images'},
		{'id':221,'forum_url':'https://t66y.com/thread0806.php?fid=22&type=1','forum_type':'images'},
		{'id':23,'forum_url':'https://t66y.com/thread0806.php?fid=23','forum_type':'images'},
		{'id':25,'forum_url':'https://t66y.com/thread0806.php?fid=25','forum_type':'images'},
		{'id':2612,'forum_url':'https://t66y.com/thread0806.php?fid=26&type=12','forum_type':'images'},
		{'id':265,'forum_url':'https://t66y.com/thread0806.php?fid=26&type=5','forum_type':'images'},
		{'id':264,'forum_url':'https://t66y.com/thread0806.php?fid=26&type=4','forum_type':'images'},
		{'id':263,'forum_url':'https://t66y.com/thread0806.php?fid=26&type=3','forum_type':'images'},
		{'id':262,'forum_url':'https://t66y.com/thread0806.php?fid=26&type=2','forum_type':'images'},
		{'id':261,'forum_url':'https://t66y.com/thread0806.php?fid=26&type=1','forum_type':'images'},
		{'id':2712,'forum_url':'https://t66y.com/thread0806.php?fid=27&type=12','forum_type':'images'},
		{'id':275,'forum_url':'https://t66y.com/thread0806.php?fid=27&type=5','forum_type':'images'},
		{'id':274,'forum_url':'https://t66y.com/thread0806.php?fid=27&type=4','forum_type':'images'},
		{'id':273,'forum_url':'https://t66y.com/thread0806.php?fid=27&type=3','forum_type':'images'},
		{'id':272,'forum_url':'https://t66y.com/thread0806.php?fid=27&type=2','forum_type':'images'},
		{'id':271,'forum_url':'https://t66y.com/thread0806.php?fid=27&type=1','forum_type':'images'}]

		for num in range(len(forum_list)):
			self.op_forum(**forum_list[num])

	def op_forum(self,id,forum_url,forum_type):
		'''处理翻页'''
		next_text = self.t66y_config['forum_next_text']
		print "get_content",forum_url

		try:
			content = self.wget.get_content(forum_url)
		except:
			print content
			return False

		#分析页面thread
		self.parse_forum(content,id,forum_type)

		# if int(forum_url[-1:]) == 2:
		# 	return True
		#翻页
		bsobj = BS(content,from_encoding="gb18030")

		next_obj = bsobj.find(text=next_text)
		if not next_obj:
			return False
		if next_obj.parent.attrs['href'] == 'javascript:#':
			return False
		next_url = self.t66y_config['domain'] + next_obj.parent.attrs['href']
		self.op_forum(id,next_url,forum_type)
		return True

	def parse_forum(self,content_html,fid,forum_type):
		'''分析页面,必要信息提交给thread'''
		bsobj = BS(content_html,from_encoding="gb18030")
		threads = bsobj.findAll("td",{"class":"tal"})
		for thread in threads:
			thread_dict = {}
			thread_dict['fid'] = fid
			thread_dict['forum_type'] = forum_type
			thread_dict['thread_url'] = self.t66y_config['domain'] + thread.a.attrs['href']
			thread_dict['title'] = thread.a.string

			sql = "select count(*) from pages where url='%s'" % (thread_dict['thread_url'])
			count_tuple = self.db.selectone(sql)
			if count_tuple[0]:
				continue

			image_page(**thread_dict)
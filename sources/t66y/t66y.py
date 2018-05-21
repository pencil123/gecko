#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import sys
import json
import time
import types
from bs4 import BeautifulSoup as BS

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
		self.op_index()
		#print self.wget.get_content(self.domain)

	def op_index(self):
		forum_list =[{'id':16,'forum_url':'https://t66y.com/thread0806.php?fid=16&search=&page=41','forum_type':'images'},
		{'id':20,'forum_url':'https://t66y.com/thread0806.php?fid=20','forum_type':'text'}]

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
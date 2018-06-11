#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import json
import time
import os
import re
import datetime
import types
from bs4 import BeautifulSoup as BS

from libs.wget import wget
from libs.mysqlconn import MysqlConn
from libs.utils import utils

reload(sys)
sys.setdefaultencoding('utf-8')
class modify_content(object):
	def __init__(self):
		self.db =MysqlConn()
		self.wget = wget()
		self.utils = utils('ads')

	def traversal(self):
		link_get_string = "select id,content from raw_content where status =1 limit 200";
		result = self.db.selectall(link_get_string)

		while len(result):
			for num in range(len(result)):
				url_id,content = result[num]
				print url_id
				self.get_link(content)
				self.db.query2("update raw_content set status = 11 where id = %s",(url_id,))
			result = self.db.selectall(link_get_string)

	def get_link(self,content):
		bsobj = BS(content,from_encoding="gb18030")
		for tags in bsobj.descendants:
			#print tags.name
			if 'a' == tags.name and 'href' in tags.attrs:
				#不存在href属性的链接不处理
				result = self.db.query2("update links set count = count +1 where link = %s",(tags.attrs['href'],))
				print result
				if result == 0:
					self.db.query2("insert into links(link) values(%s)",(tags.attrs['href'],))
				continue
			else:
				continue
		# imgs_list = []
		# content = ''
		# imgsurl_tag = ['data-src','src']

		# #html标签逐层遍历
		# tmp_cont_before = ''
		# for tags in body.descendants:
		# #广告处理
		# 	if 'a' == tags.name and 'href' in tags.attrs:
		# 		#不存在href属性的链接不处理
		# 		if not self.utils.ads(tags.attrs['href']):
		# 			content = content + tags.prettify()
		# 			result = self.db.query2("update links set count = count +1 where link = %s",(tags.attrs['href'],))
		# 			print result
		# 			if result == 0:
		# 				self.db.query2("insert into links(link) values(%s)",(tags.attrs['href'],))

		# 		continue
		# 	else:
		# 		continue

		# 	if 'img' == tags.name and 'data-link' in tags.attrs:
		# 		if not self.utils.ads(tags.attrs['data-link']) and 'src' in tags.attrs:
		# 			content = content + '<img src=\"' + tags.attrs['src'].encode('utf8') + '\" >'
		# 			self.db.query2("insert into images(url) value(%s)",(tags.attrs['src'],))
		# 		continue
		# 	else:
		# 		if 'src' in tags.attrs:
		# 			content = content + '<img src=\"' + tags.attrs['src'].encode('utf8') + '\" >'
		# 			self.db.query2("insert into images(url) value(%s)",(tags.attrs['src'],))
		# 		continue


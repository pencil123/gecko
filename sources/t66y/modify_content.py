#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import json
import time
import os
import re
import datetime
import types
import math
from bs4 import BeautifulSoup as BS

from libs.wget import wget
from libs.utils import connect
from libs.utils import utils

reload(sys)
sys.setdefaultencoding('utf-8')
class modify_content(object):
	def __init__(self):
		self.conn,self.cursor = connect()
		self.wget = wget()
		self.utils = utils('ads')

	def traversal(self):
		count_sql = "select count(*) from raw_content where status=1"
		self.cursor.execute(count_sql)
		count_num = self.cursor.fetchone()[0]

		if not count_num:
			return False
		print count_num

		for range_num in range(int(math.ceil(count_num/200))):
			link_get_string = "select id,content from raw_content where status =1 limit 200";
			self.cursor.execute(link_get_string)
			result = self.cursor.fetchall()
			for num in range(len(result)):
				url_id,content = result[num]
				self.get_link(content,url_id)
				self.cursor.execute("update raw_content set status = 11 where id = %s",(url_id,))

	def get_link(self,content,url_id):
		bsobj = BS(content,from_encoding="gb18030")
		print url_id
		for tags in bsobj.descendants:
			#print tags.name
			if 'a' == tags.name and 'href' in tags.attrs:
				#不存在href属性的链接不处理
				raw_link = tags.attrs['href']
				print raw_link
				pattern = re.match(r'http://www.viidii.info/\?(.*)\&z$',raw_link)
				if pattern:
					link = pattern.group(1)
					link = link.replace("______",".")
					print link,url_id
					self.cursor.execute("update links set count = count +1 where link = %s",(link,))
					if not self.cursor.rowcount:
						try:
							self.cursor.execute("insert into links(link) values(%s)",(link,))
						except:
							pass
				else:
					try:
						self.cursor.execute("insert into links(link,status) values(%s,0)",(raw_link,))
					except:
						print raw_link,url_id
			else:
				continue
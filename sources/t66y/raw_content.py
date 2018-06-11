#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
from bs4 import BeautifulSoup as BS

from libs.wget import wget
from libs.utils import connect

reload(sys)
sys.setdefaultencoding('utf-8')
class raw_content(object):
	def __init__(self):
		'''
		parameter:thread_dict['url']
		parameter:thread_dict['title']
		'''
		self.conn,self.cursor =connect()
		self.wget = wget()

	def download(self,thread_url,fid):
		#页面抓取失败，返回状态不是200
		try:
			content = self.wget.get_content(thread_url)
		except Exception, e:
			self.cursor.execute("insert into raw_content(url,source,fid,status,content) values(%s,'t66y',%s,2,%s)",(thread_url,int(fid)),str(e))
			return False
		if len(content) < 2014:
			self.cursor.execute("insert into raw_content(url,source,fid,status) values(%s,'t66y',%s,3)",(thread_url,int(fid)))
			return False
		bsobj = BS(content,from_encoding="gb18030")
		body = bsobj.find("div",{'class':'tpc_content do_not_catch'})
		if not body:
			self.cursor.execute("insert into raw_content(url,source,fid,status) values(%s,'t66y',%s,4)",(thread_url,int(fid)))
			return False

		self.cursor.execute("insert into raw_content(url,content,source,fid) values(%s,%s,'t66y',%s)",(thread_url,body,int(fid)))
		return True
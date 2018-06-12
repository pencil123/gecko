#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
from bs4 import BeautifulSoup as BS

from libs.wget import wget
from libs.utils import connect
from libs.utils import modify_title

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
		#print thread_url
		bsobj = BS(content,from_encoding="gb18030")
		if bsobj.title:
			title = modify_title(bsobj.title.string)
		else:
			title = "404 not found"
			self.cursor.execute("update raw_content set title=%s where id=%s",('404 not found',fid))
		body = bsobj.find("div",{'class':'tpc_content do_not_catch'})

		if len(content) < 2014:
			self.cursor.execute("insert into raw_content(url,source,fid,status,title) values(%s,'t66y',%s,3,%s)",(thread_url,int(fid),title))
			return False

		if not body:
			self.cursor.execute("insert into raw_content(url,source,fid,status,title) values(%s,'t66y',%s,4,%s)",(thread_url,int(fid),title))
			return False

		self.cursor.execute("insert into raw_content(url,content,source,fid,title) values(%s,%s,'t66y',%s,%s)",(thread_url,body,int(fid),title))
		return True
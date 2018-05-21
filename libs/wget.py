#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import pycurl
import sys
import json
import re
import types
import os
import time
import datetime
import codecs
import random
import string
try:
	from io import BytesIO
except ImportError:
	from StringIO import StringIO as BytesIO

reload(sys)
sys.setdefaultencoding('utf-8')

class wget(object):
	def __init__(self):
		self.string_peferer = ''
		self.imgs_list = []
		self.imgs_dirs = 0
		self.handler = pycurl.Curl()
		self.handler.setopt(pycurl.USERAGENT,"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36")
		self.handler.setopt(pycurl.COOKIEFILE, "cookie_file_name")
		self.handler.setopt(pycurl.HTTPHEADER,['text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'])
		self.handler.setopt(pycurl.CONNECTTIMEOUT, 160)
		self.handler.setopt(pycurl.TIMEOUT, 5)
		self.handler.setopt(pycurl.FORBID_REUSE, 1)
		self.handler.setopt(pycurl.FOLLOWLOCATION, 1)
		self.handler.setopt(pycurl.MAXREDIRS, 3)
		self.handler.setopt(pycurl.NOPROGRESS, 1)
		self.handler.setopt(pycurl.DNS_CACHE_TIMEOUT,30)
		self.handler.setopt(pycurl.NOSIGNAL, 1)
		self.handler.setopt(pycurl.SSL_VERIFYPEER, 0)
		self.handler.setopt(pycurl.SSL_VERIFYHOST, 0)
		#self.handler.setopt(pycurl.SSLVERSION, 3)

	def set_proxy(self,str_uri,userandpass=''):
		self.handler.setopt(pycurl.PROXY,str_uri)
		if not userandpass:
			self.handler.setopt(pycurl.PROXYUSERPWD,userandpass)

	def set_peferer(self,str_peferer=''):
		if str_peferer :
			str_peferer = self.string_peferer
		self.handler.setopt(pycurl.REFERER,str_peferer)

	def get_content(self,str_url):
		self.handler.setopt(pycurl.TIMEOUT, 20)
		content_buf = BytesIO()
		self.set_peferer()
		self.handler.setopt(pycurl.WRITEFUNCTION,content_buf.write)
		self.handler.setopt(pycurl.URL,str_url)
		self.handler.perform()
		http_status = self.handler.getinfo(pycurl.HTTP_CODE)
		#状态如果不是200
		if 200 != http_status:
			print http_status
			return http_status

		self.string_peferer = str_url
		content = content_buf.getvalue()
		content_buf.close()
		return content

	def down_img(self,imgfile_list):
		'''
		parameter:imgs_url  imgs_file
		'''
		for num in range(len(imgfile_list)):
			img_url = imgfile_list[num][0]
			img_file = imgfile_list[num][1]
			content_buf = BytesIO()
			self.handler.setopt(pycurl.WRITEFUNCTION,content_buf.write)
			self.handler.setopt(pycurl.URL,img_url)
			try:
				self.handler.perform()
			except:
				return True
			img_content =content_buf.getvalue()
			content_buf.close()
			self.__write_file(img_content,img_file)
		return True

	def __write_file(self,img_content,img_file):
		file_handler = open(img_file,'wb')
		file_handler.write(img_content)
		file_handler.close()
		return True
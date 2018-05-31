#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import re
from libs.mysqlconn import MysqlConn

class utils(object):
	def __init__(self,functs):
		self.db = MysqlConn()
		if 'ads' == functs:
			str_sql = "select domain from ads where status=1"
			ads_domain = self.db.selectall(str_sql)
			pattern = r'' + ads_domain[0][0]
			for num in range(1,len(ads_domain)):
				pattern = pattern + '|' + ads_domain[num][0]
			self.rep = re.compile(pattern,re.DOTALL)

	def ads(self,url):
		match = self.rep.search(url)
		if match:
			return True
		else:
			return False


	# def del_bracket(str_raw):
	# 	str_raw = str_raw.replace(' ','')
	# 	handler = re.compile('\[.*?\]' )
	# 	return handler.sub('',str_raw)

	# def blackurl():
	# 	blackurl = set()
	# 	handler = MysqlConn()
	# 	str_sql = "select url from attach_black"
	# 	result = handler.selectall(str_sql)
	# 	for num in range(len(result)):
	# 		blackurl.add(result[num][0].encode('utf8'))
	# 	return blackurl


#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import sys
import json
import time
from bs4 import BeautifulSoup as BS

from libs.wget import wget
from libs.mysqlconn import MysqlConn

class Guess(object):
	def __init__(self):
		self.wget = wget()
		self.db = MysqlConn()
		# max_sql = 'select max(url_num) from pages'
		# max_num = self.db.selectone(max_sql)[0]

		# min_sql = 'select max(pagenum) from guess'
		# min_num = self.db.selectone(min_sql)[0]
		# if not min_num:
		# 	min_num = 30611
		# print max_num,min_num

		# for num in range(max_num,min_num,-1):
		# 	sql = "select count(*) from pages where url_num = %s" % (num)
		# 	count_tuple = self.db.selectone(sql)
		# 	if not count_tuple[0]:
		# 		guess_date_sql = "select url_date from pages where url_num < %s order by url_num desc limit 1" % (num)
		# 		guess_date = self.db.selectone(guess_date_sql)[0]

		# 		sql = "insert into guess (pagedate,pagenum) values (%s,%s)" % (guess_date,num)
		# 		#print sql
		# 		self.db.query(sql)

		for num100 in range(31541):
			sql = 'select pagedate,pagenum from guess where pagenum<3040909 order by id asc limit %s,100' % (100*num100)
			pagenum_tuple = self.db.selectall(sql)
			for num in range(len(pagenum_tuple)):
				pagedate,pagenum = pagenum_tuple[num]
				self.url_page(pagedate,pagenum)
				print pagedate,pagenum


	def url_page(self,pagedate,pagenum):
		forum_url = [
		'https://t66y.com/htm_data/2/',
		'https://t66y.com/htm_data/4/',
		'https://t66y.com/htm_data/5/',
		'https://t66y.com/htm_data/7/',
		'https://t66y.com/htm_data/8/',
		'https://t66y.com/htm_data/15/',
		'https://t66y.com/htm_data/16/',
		'https://t66y.com/htm_data/20/',
		'https://t66y.com/htm_data/21/',
		'https://t66y.com/htm_data/22/',
		'https://t66y.com/htm_data/23/',
		'https://t66y.com/htm_data/25/',
		'https://t66y.com/htm_data/26/',
		'https://t66y.com/htm_data/27/',
		'https://t66y.com/htm_data/10/']

		for new_date in (pagedate,pagedate-1,pagedate+1):
			hit = False
			for url_num in range(len(forum_url)):
				url = forum_url[url_num] + str(new_date) + '/' + str(pagenum) + ".html"
				try:
					if '404' != self.wget.get_content(url):
						hit = True
						self.url_success(url)
						break
				except:
					continue
			if hit:
				break
	def url_success(self,url):
		url_sql = "insert into url(url) value('%s')" % (url)
		self.db.query(url_sql)

				# url = forum_url[num] + "0707/" + str(pagenum) + ".html"
				# if '404' != self.wget.get_content(url):
				# 	print url
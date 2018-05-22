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
		forum_url = [
		'https://t66y.com/htm_data/2/',
		'https://t66y.com/htm_data/4/',
		'https://t66y.com/htm_data/5/',
		'https://t66y.com/htm_data/7/',
		'https://t66y.com/htm_data/8/',
		'https://t66y.com/htm_data/10/',
		'https://t66y.com/htm_data/15/',
		'https://t66y.com/htm_data/16/',
		'https://t66y.com/htm_data/20/',
		'https://t66y.com/htm_data/21/',
		'https://t66y.com/htm_data/22/',
		'https://t66y.com/htm_data/25/',
		'https://t66y.com/htm_data/26/',
		'https://t66y.com/htm_data/27/']
		self.wget = wget()
		self.db = MysqlConn()

		max_num = 3150510

		for num in range(max_num,50534,-1):
			sql = "select count(*) from url where pagenum = %s" % (num)
			count_tuple = self.db.selectone(sql)
			if not count_tuple[0]:
				sql = "insert into guess (pagenum) values (%s)" % (num)
				self.db.query(sql)

		# for pagenum in range(46456,50534):
		# 	for num in range(len(forum_url)):
		# 		url = forum_url[num] + "0707/" + str(pagenum) + ".html"
		# 		if '404' != self.wget.get_content(url):
		# 			print url
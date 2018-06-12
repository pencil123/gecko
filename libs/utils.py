#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import re
import MySQLdb

def connect():
	mysql_var = {'host':"localhost",    # your host, usually localhost
					 'user':"gecko",         # your username
					 'passwd':"gecko",  # your password
					 'db':"gecko1",
					 'charset':'utf8'}
	conn=MySQLdb.connect(**mysql_var)
	conn.set_character_set('utf8')
	conn.autocommit(True)
	cursor=conn.cursor()
	cursor.execute('SET NAMES utf8;')
	cursor.execute('SET CHARACTER SET utf8;')
	cursor.execute('SET character_set_connection=utf8;')
	return (conn,cursor)

def modify_title(title):
	if title.endswith('t66y.com'):
		title_list1 = title.split('-')
		new_list = title_list1[:-2]
		title = ' '.join(str(e) for e in new_list)

	match = re.match(r'(.*).[V|v][I|i][P|p](.*)$',title)
	if match:
		title = match.group(1)
		if len(match.groups()) > 1 and len(match.group(2)) > 20:
			title = title + "VIP " + match.group(2)
	return title


class utils(object):
	def __init__(self,functs):
		self.conn,self.cursor = connect()
		if 'ads' == functs:
			str_sql = "select domain from ads where status=1"
			self.cursor.execute(str_sql)
			ads_domain = self.cursor.fetchall()
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
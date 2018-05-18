#!/usr/bin/env python
#-*- coding: UTF-8 -*-
from MySQLdb import escape_string
from libs.mysqlconn import MysqlConn

class MySql(object):
	def __init__(self):
		self.conn = MysqlConn()

	def forum(self,platform):
		'''返回频道列表'''
		str_sql = "select id,url,type,content_type from forum where platform='%s' and status =0 " % (platform)
		result = self.conn.selectall(str_sql)
		forum_list = []
		for num in range(len(result)):
			forum_dict = {}
			forum_single = result[num]
			#print forum_single
			forum_dict['id'] = forum_single[0]
			if forum_single[2]:
				forum_dict['forum_url'] = forum_single[1] + forum_single[2]
			else:
				forum_dict['forum_url'] = forum_single[1]
			forum_dict['forum_type'] = forum_single[3]
			forum_list.append(forum_dict)
		return forum_list

	def thread(self,fid,url,title,content=''):
		'''
		插入
		'''
		if content:
			str_sql = "insert into thread (fid,url,title,content) values(%s,%s,%s,%s)"
			str_tuple = (fid,url,title,content)
		else:
			str_sql = "insert into thread (fid,url,title) values(%s,%s,%s)"
			str_tuple = (fid,url,title)
		result = self.conn.query2(str_sql,str_tuple)
		return result

	def thread_exist(self,fid,url):
		#判断是否存在
		str_sql = "select count(*) from thread where fid=%s and url='%s'" % (fid,url)
		count = self.conn.selectone(str_sql)
		if count[0] == 1:
			return True
		if not count[0]:
			return False

	def thread_kongbody(self,fid,url):
		#判断是否存在
		str_sql = "insert into thread (fid,url,status) values(%s,%s,%s)"
		count = self.conn.query2(str_sql,(fid,url,3))
		return True


	def attach(self,attach_list,tid):
		for num in range(len(attach_list)):
			str_sql = "insert into attach (url,tid) values('%s',%s)" % (attach_list[num],tid)
			if 1062 == self.conn.query(str_sql):
				str_sql = "update attach set count = count +1 where url = '%s'" % (attach_list[num])
			self.conn.query(str_sql)
		return True
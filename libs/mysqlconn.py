#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import MySQLdb

#from config.config import mysql_var

class MysqlConn(object):
	def __init__(self):
		mysql_var = {'host':"localhost",    # your host, usually localhost
                     'user':"gecko",         # your username
                     'passwd':"gecko",  # your password
                     'db':"gecko1",
                     'charset':'utf8'}
		self.conn=MySQLdb.connect(**mysql_var)
		self.conn.set_character_set('utf8')
		self.cursor=self.conn.cursor()
		self.cursor.execute('SET NAMES utf8;')
		self.cursor.execute('SET CHARACTER SET utf8;')
		self.cursor.execute('SET character_set_connection=utf8;')
		#self.cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;")
	def selectall(self,str_sql):
		try:
			self.cursor.execute(str_sql)
		except Exception, e:
			print 'str(Exception):\t', str(Exception)
			print 'str(e):\t\t', str(e)
			print 'repr(e):\t', repr(e)
			print 'e.message:\t', e.message
			# print 'traceback.print_exc():'; traceback.print_exc()
			# print 'traceback.format_exc():\n%s' % traceback.format_exc()
		result = self.cursor.fetchall()
		return result
	def selectone(self,str_sql):
		try:
			self.cursor.execute(str_sql)
		except Exception, e:
			print 'str(Exception):\t', str(Exception)
			print 'str(e):\t\t', str(e)
			print 'repr(e):\t', repr(e)
			print 'e.message:\t', e.message
			# print 'traceback.print_exc():'; traceback.print_exc()
			# print 'traceback.format_exc():\n%s' % traceback.format_exc()
		result = self.cursor.fetchone()
		return result
	def query(self,str_sql):
		try:
			self.cursor.execute(str_sql)
		except MySQLdb.IntegrityError as e:
			return 1062
		except Exception,e:
			print str(Exception)
			print str(e)
			print (str_sql)
			return False
		self.conn.commit()
		id = self.cursor.lastrowid
		return id
	def query2(self,str_sql,var_tuple):
		try:
			self.cursor.execute(str_sql,var_tuple)
		except Exception,e:
			print str(e)
			print (str_sql)
			return False
		self.conn.commit()
		id = self.cursor.lastrowid
		return id
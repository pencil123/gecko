#!/usr/bin/env python
#-*- coding: UTF-8 -*-
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
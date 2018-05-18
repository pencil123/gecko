#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import re

from libs.mysqlconn import MysqlConn

def del_bracket(str_raw):
	str_raw = str_raw.replace(' ','')
	handler = re.compile('\[.*?\]' )
	return handler.sub('',str_raw)

def blackurl():
	blackurl = set()
	handler = MysqlConn()
	str_sql = "select url from attach_black"
	result = handler.selectall(str_sql)
	for num in range(len(result)):
		blackurl.add(result[num][0].encode('utf8'))
	return blackurl

def ads():
	ads = {}
	handler = MysqlConn()

	str_sql = "select url from ads where status='img'"
	img_ads = handler.selectall(str_sql)
	imgs= set()
	for num in range(len(img_ads)):
		imgs.add(img_ads[num][0])

	str_sql = "select url from ads where status='a'"
	a_ads = handler.selectall(str_sql)
	addrs= set()
	for num in range(len(a_ads)):
		addrs.add(a_ads[num][0])

	ads['imgs'] = imgs
	ads['addrs'] = addrs
	return ads

blackurl_imgs = blackurl()
print blackurl_imgs
ads = ads()
print ads
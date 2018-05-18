#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import sys
import json
import re
import time
from spider import curl_headler
from mysql_base import mysqlbase as mysqldb
from bs4 import BeautifulSoup as BS

class ck180():
	def __init__(self):
		self.mdb = mysqldb()
		self.domain = "http://www.ck180.net/"

	def channels_update(self):
		'''更新频道的主函数'''
		sql_str = "select channel,bbsfid,spidertype from config"
		channels = self.mdb.selectall(sql_str)
		for num_channels in range(len(channels)):
			self.bbsfid = channels[num_channels][1]
			channel_url = self.domain + channels[num_channels][0]
			self.channel_index(channel_url,channels[num_channels][2])

	def channel_index(self,channel_url,page_type):
		'''更新单个频道函数；包含频道的下一页'''
		channel_curl = curl_headler(channel_url)
		print channel_url
		Content = channel_curl.perform()
		#print Content
		bsobj = BS(Content)
		if page_type == 1:
			videoslist = bsobj.findAll("h3",{"class":"p-meta-title"})
		elif page_type ==2:
			videoslist = bsobj.findAll("p",{"class":{"s2 no","s2 n3"}})
		for video in videoslist:
			#print type(video)
			self.video_url = video.a.attrs['href']
			self.video_name = video.a.attrs['title']
			self.table_infos_insert()

		next_url = self.channel_next_index(bsobj)
		print next_url
		if next_url:
			self.channel_index(next_url,page_type)
		else :
			return True


	def channel_next_index(self,bsobj):
		'''返回频道下一页的连接'''
		next_url = bsobj.find("a",{"class":"nextpostslink"})
		try:
			locals().has_key("next_url.attrs['href']")
			return next_url.attrs['href']
		except:
			return False

	def table_infos_insert(self):
		'''插入各频道的电影'''
		sql_str = "select * from infos where url = '%s'" % (self.video_url)
		print sql_str
		result = self.mdb.selectone(sql_str)
		if result is None:
			sql_str = "insert into infos (url,name,bbsfid) values(%s,%s,%s)"
			self.mdb.query2(sql_str,(self.video_url,self.video_name,self.bbsfid))


	def videos_update(self):
		'''更新电影的主函数'''
		sql_str = "select url,bbsfid,id from infos where status = 0"
		results = self.mdb.selectall(sql_str)
		for num_video in range(len(results)):
			video_url = results[num_video][0]
			print video_url
			self.video_html(video_url,results[num_video][1])
			self.update_db(results[num_video][2])

		print results




	def video_html(self,video_url,bbsfid):
		'''更新单个电影'''
		video_curl = curl_headler(video_url)
		Content = video_curl.perform()
		print Content
		#print Content
		try:
			bsobj = BS(Content)
		except:
			print Content
		dtimg = bsobj.findAll("div",{"class":"dt"})
		img_url = dtimg[0].img.attrs['src'].split('?')[0]
		img_curl = curl_headler(img_url)
		self.imgname = img_curl.download("img")

		dtinfo = bsobj.findAll("div",{"class":"video-info"})
		self.video_info =  dtinfo[0].get_text()
		self.bbsfid = bbsfid

		if bbsfid == 45:
			self.filename = None
		else :
			bturlint_pattern = re.compile(r'net\/(.*?)\.html',re.M)
			bt_int = bturlint_pattern.findall(video_url)
			self.video_btfile(bt_int[0])

	def video_btfile(self,num_html):
		'''更新单个电影的bt文件'''
		ver = time.strftime("%Y%m%d%H%M%S")
		bturl = "http://api.xn123.cn/api/json_" + num_html +".json?ver=" + ver
		print bturl
		curl = curl_headler(bturl)
		info_str = curl.perform()
		try:
			info_str = info_str.replace(":null",":None")
		except:
			pass
		print info_str
		info_json = eval(info_str)
		self.ed2k = None
		if info_json[0].has_key('bturl'):
			btfile_url = "http://ck180.hzxdr.cn/down.php?" + info_json[0]['bturl']
			btcurl = curl_headler(btfile_url)
			self.filename = btcurl.download("bt",".torrent")
			self.ed2k = None
		elif info_json[0].has_key('nameed2k'):
			self.filename = None
			self.ed2k = info_str


	def update_db(self,video_id):
		'''更新完电影；更新数据库'''
		str_sql = "update infos set content = %s,image= %s,btfilename= %s,ed2k= %s,status= %s,bbsfid= %s where id = %s"
		self.mdb.query2(str_sql,(self.video_info,self.imgname,self.filename,self.ed2k,1,self.bbsfid,video_id))


	def videos_ed2k(self):
		'''修补ed2k缺失问题'''
		sql_str = "select url,bbsfid,id from infos where btfilename is NULL and ed2k is null"
		results = self.mdb.selectall(sql_str)
		for num_video in range(len(results)):
			video_url = results[num_video][0]
			bturlint_pattern = re.compile(r'com\/(.*?)\.html',re.M)
			bt_int = bturlint_pattern.findall(video_url)
			self.video_btfile(bt_int[0])
			self.update_ed2k(results[num_video][2])

	def update_ed2k(self,video_id):
		'''修补ed2k 更新数据库'''
		str_sql = "update infos set ed2k= %s where id = %s"
		self.mdb.query2(str_sql,(self.ed2k,video_id))

		
test = ck180()
test.channels_update()
test.videos_update()
test.videos_ed2k()
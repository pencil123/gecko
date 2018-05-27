#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import json
import time
import os
import re
import datetime
import types
from bs4 import BeautifulSoup as BS

from libs.wget import wget
from libs.mysqlconn import MysqlConn
reload(sys)
sys.setdefaultencoding('utf-8')
class image_page(object):
	def __init__(self,thread_url,title,forum_type,fid):
		'''
		parameter:thread_dict['url']
		parameter:thread_dict['title']
		'''
		self.db =MysqlConn()
		self.wget = wget()
		url = thread_url
		title = title
		print url
		#title 为空；舍弃
		if not title:
			return None

		pattern=re.compile(r'https://t66y.com/htm_data/(\d+)/(\d+)/(\d+)\.html',re.DOTALL)
		match = pattern.match(url)
		if match:
			url_id,url_date,url_num = match.groups()
		else:
			return None

		self.db.query2("insert into pages(fid,url,url_date,url_num,title) values(%s,%s,%s,%s,%s)",(int(url_id),url,int(url_date),int(url_num),title))
		return None
		#thread已经存在；则直接返回
		# if self.db.thread_exist(fid=fid,url=url):
		# 	return True

		#页面抓取失败，返回状态不是200
		try:
			content = self.wget.get_content(url)
		except Exception, e:
			print 'str(e):\t\t', str(e)
			return None
		if len(content) < 2014:
			return None
		bsobj = BS(content,from_encoding="gb18030")
		body = bsobj.find("div",{'class':'tpc_content do_not_catch'})
		if not body:
		# 	self.db.thread_kongbody(fid=fid,url=url)
			return None

		self.db.query2("insert into pages(fid,url,url_date,url_num,title,content) values(%s,%s,%s,%s,%s,%s)",(int(url_id),url,int(url_date),int(url_num),title,body))
		return None


		#区分内容类型
		if forum_type == 'images':
			#tid = self.db.thread(fid=fid,url=url,title=title)
			content = self.get_images(body,0)#tid
		print content
		print content.encode('utf8')
		self.db.query2("insert into pages(url,title,content) values(%s,%s,%s)",\
			(url,title,content))
		return None


	def get_images(self,body,fid):
		imgs_list = []
		content = ''
		imgsurl_tag = ['src','data-src']

		#html标签逐层遍历
		tmp_cont_before = ''
		for tags in body.descendants:
			if 'input' == tags.name:
			#下载连接是否在黑名单中
				# if img.attrs['src'] in blackurl_imgs:
				# 	continue

				#判断type是否为图片
				image = False
				if 'type' in tags.attrs and 'image' == tags.attrs['type']:
					image = True
				else:
					continue

				#从imgsurl_tag中获取图片url
				tag_srcname = filter(lambda tag:tag in tags.attrs,imgsurl_tag)
				if len(tag_srcname) >=1:
					src_name = tag_srcname[0]
				else:
					continue
				if len(tags.attrs[src_name]) >= 300:
					continue
				imgs_list.append((tags.attrs[src_name].encode('utf8'),image))
				tmp_cont = "<img>" + tags.attrs[src_name].encode('utf8') + "</img>"
				#print tmp_cont,type(tmp_cont)
				content = content + tmp_cont + '\r\n'
			else:
				tmp_cont = tags.string
				if tmp_cont and (tmp_cont != tmp_cont_before):
					content = content + tmp_cont + '\r\n'
					tmp_cont_before = tmp_cont
		self.create_imgfile(imgs_list)
		return content

	def create_imgfile(self,imgs_list):
		# print "down_img",imgs_list
		#self.wget.down_img(imgs_list,'t66y/')

		#生成存储文件
		realpath = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
		self.img_dir = realpath + '/download/' + datetime.datetime.today().strftime('%s')
		self.__create_dir(self.img_dir)

		#download images file
		imgfile_list = []
		for num in range(len(imgs_list)):
			image_url = imgs_list[num][0]
			image_type = imgs_list[num][1]

			type_file = image_url.split('.')[-1]
			if len(type_file) > 4:
				type_file = image_url.split('&')[-1]
				if len(type_file) > 4 and image_type:
					type_file = 'jpg'
				else:
					continue
					
			img_file = self.img_dir + '/' + str(num) + '.' + type_file
			imgfile_list.append((image_url,img_file))
		self.wget.down_img(imgfile_list)

		#insert information into database table images
		for num in range(len(imgfile_list)):
			self.db.query2("insert into images(url,filename) values(%s,%s)",(imgfile_list[num][0].encode('utf8'),imgfile_list[num][1].encode('utf8')))

	def __create_dir(self,dir_path):
		if os.path.exists(dir_path):
			return True
		if os.makedirs(dir_path):
			return True
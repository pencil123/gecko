#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import sys
import json
import time
import os
import datetime
import types
from bs4 import BeautifulSoup as BS

from libs.wget import wget
from libs.mysqlconn import MysqlConn

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
			return False
		#thread已经存在；则直接返回
		# if self.db.thread_exist(fid=fid,url=url):
		# 	return True

		#页面抓取失败，返回状态不是200
		try:
			content = self.wget.get_content(url)
		except Exception, e:
			print 'str(e):\t\t', str(e)
			return False
		bsobj = BS(content,from_encoding="gb18030")
		body = bsobj.find("div",{'class':'tpc_content do_not_catch'})
		if not body:
		# 	self.db.thread_kongbody(fid=fid,url=url)
			return None

		#区分内容类型
		if forum_type == 'images':
			#tid = self.db.thread(fid=fid,url=url,title=title)
			content = self.get_images(body,0)#tid
		# elif forum_type == 'text':
		# 	content = ''
		# 	for string in body.stripped_strings:
		# 		content += string + '\n'
		# 	#print type(content)
		# 	self.db.thread(fid=fid,url=url,title=title,content=content)
		# elif forum_type == 'multi':
		# 	self.op_multi(body,fid,url,title)

	# def op_multi(self,body,fid,url,title):
	# 	content = ''
	# 	for tag in body.children:
	# 		#print tag,'end'
	# 		if not tag.name or 'br' == tag.name or 'span' == tag.name:
	# 			continue

	# 		if 'img' == tag.name:
	# 			if tag.attrs['src'] in ads['imgs']:
	# 				continue
	# 			content += '<img src="' + tag.attrs['src'] +'" >\n'

	# 		if 'a' == tag.name:
	# 			if not tag.has_attr('href'):
	# 				continue
	# 			if tag.attrs['href'] in ads['addrs']:
	# 				continue
	# 			content += '<a href="' + tag.attrs['href'] +'" >' + tag.get_text() + "</a>\n"
	
	# 		content += tag.get_text() + '\n'
	
	# 	self.db.thread(fid=fid,url=url,title=title,content=content)

		self.db.query2("insert into pages(url,title,content) values(%s,%s,%s)",(url.encode('utf8'),title.encode('utf8'),content.encode('utf8')))
		return None


	def get_images(self,body,fid):
		imgs_list = []
		#print body.get_text()
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

				imgs_list.append((tags.attrs[src_name],image))
				tmp_cont = "<img>" + tags.attrs[src_name].encode('utf8') + "</img>"
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
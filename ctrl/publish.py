#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from config.config import discuz_var
from model.discuzapi import DiscuzAPI
from libs.mysqlconn import MysqlConn
import time
from random import randint

class Publish(object):
	def __init__(self):
		self.domain = discuz_var['domain']
		self.db = MysqlConn()
		self.count_peruser = 3
		self.user_login =False

	def register(self):
		fields = discuz_var['fields']
		str_sql = "select username,password,email,id from user_dis where status = %s" % (0,)
		users_tuple = self.db.selectall(str_sql)
		for num in range(len(users_tuple)):
			handler = DiscuzAPI(self.domain)
			username,passwd,email,user_id = users_tuple[num]
			if handler.register(username,passwd,email,fields):
				str_sql = "update user_dis set status=1 where id =%s"
				self.db.query(str_sql,(user_id,))
				handler.logout()
			del(handler)
		return True

	def random_publis(self):
		str_sql = "select id,dis_fid,content_type from forum where status =%s" % (0,)
		forums_tuple = self.db.selectall(str_sql)
		for num in range(len(forums_tuple)):
			forum_id,dis_fid,text_type = forums_tuple[num]
			if text_type == 'img':
				self.__publis_imgs(forum_id,dis_fid)

	def __publis_imgs(self,forum_id,dis_fid):
		str_sql = "select id,title from thread where fid=%s and status=%s" % (forum_id,0)
		threads_tuple = self.db.selectall(str_sql)
		for num in range(len(threads_tuple)):
			tid,title = threads_tuple[num]
			title = title[:40]
			imgs_content = u''

			str_sql = "select url from attach where tid =%s" % (tid,)
			urls_tuple = self.db.selectall(str_sql)
			if not urls_tuple:
				continue
			for url_num in range(len(urls_tuple)):
				imgs_content += u"[img]" + urls_tuple[url_num][0] + u"[/img]\n"

			if self.user_login and not num%self.count_peruser:
				discuz.logout()
				del(discuz)
				self.user_login =False

			if not self.user_login:
				discuz = self.choose_user()
			discuz.publish(dis_fid,subject=title,msg=imgs_content)
			str_sql = 'update thread set status=%s where id = %s' % (1,tid)
			self.db.query(str_sql)



	def choose_user(self):
		str_sql = "select count(*) from user_dis where status=1"
		count = self.db.selectone(str_sql)[0]
		id_choose = randint(1,count)

		str_sql = "select username,password from user_dis where id=%s" % (id_choose,)
		user_tuple = self.db.selectone(str_sql)

		handler = DiscuzAPI(self.domain)
		handler.login(user_tuple[0],user_tuple[1])
		self.user_login =True
		return handler
			# if not urls_tuple:
			# 	return False



# users_tuple = db.selectall(str_sql)

# #handler = DiscuzAPI(domain)
# email = set()
# for num in range(len(users_tuple)):
# 	user_info = users_tuple[num]
# 	if user_info[2] in email:
# 		str_sql = "delete from user_dis where id = %s" % (user_info[3])
# 		db.query(str_sql)
# 	else:
# 		email.add(user_info[2])



# 	handler = DiscuzAPI(domain)
# 	user_info = users_tuple[num]
# 	print user_info[0]
# 	if not handler.login(user_info[0],user_info[1]):
# 	    false_num +=1
# 	    if false_num ==5:
# 	        break
# 	    str_sql = "update user_dis set status =0 where id = %s" % (user_info[3])
# 	    db.query(str_sql)
# 	handler.logout()
# 	del(handler)
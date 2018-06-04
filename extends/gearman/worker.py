#!/usr/bin/env python2.7
# -*- encoding: utf-8; py-indent-offset: 4 -*-

import gearman
import time
from bs4 import BeautifulSoup as BS

from libs.wget import wget
from libs.mysqlconn import MysqlConn


gm_worker = gearman.GearmanWorker(['localhost:4730'])

# def task_listener_reverse(gearman_worker, gearman_job):
# 	time.sleep(1)
# 	print 'Reversing string: ' + gearman_job.data
# 	return gearman_job.data[::-1]

class Guess(object):
	def __init__(self):
		self.wget = wget()
		self.db = MysqlConn()

	def url_page(self,gearman_worker, gearman_job):
		data_list = gearman_job.data.split('-')
		pagedate = int(data_list[0])
		pagenum = int(data_list[1])
		print pagedate,pagenum
		forum_url = [
		'https://t66y.com/htm_data/2/',
		'https://t66y.com/htm_data/4/',
		'https://t66y.com/htm_data/5/',
		'https://t66y.com/htm_data/7/',
		'https://t66y.com/htm_data/8/',
		'https://t66y.com/htm_data/15/',
		'https://t66y.com/htm_data/16/',
		'https://t66y.com/htm_data/20/',
		'https://t66y.com/htm_data/21/',
		'https://t66y.com/htm_data/22/',
		'https://t66y.com/htm_data/23/',
		'https://t66y.com/htm_data/25/',
		'https://t66y.com/htm_data/26/',
		'https://t66y.com/htm_data/27/',
		'https://t66y.com/htm_data/10/']

		for new_date in (pagedate,pagedate-1,pagedate+1):
			hit = False
			for url_num in range(len(forum_url)):
				url = forum_url[url_num] + str(new_date) + '/' + str(pagenum) + ".html"
				#print url
				try:
					if '404' != self.wget.get_content(url):
						hit = True
						#print "get true"
						self.url_success(url)
						break
				except:
					continue
			if hit:
				break
		return 'True'


	def url_success(self,url):
		url_sql = "insert into url(url) value('%s')" % (url)
		self.db.query(url_sql)


handler = Guess()
# gm_worker.set_client_id is optional
gm_worker.set_client_id('worker')
gm_worker.register_task('reverse', handler.url_page)

# Enter our work loop and call gm_worker.after_poll() after each time we timeout/see socket activity
gm_worker.work()
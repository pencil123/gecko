#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import sys
import json
import time
from bs4 import BeautifulSoup as BS

from libs.wget import wget
from model.mysql import MySql
from libs.utils import del_bracket
from config.config import marry_var,proxy_var


class MerryGuess(object):
	def __init__(self):
		self.domain = marry_var['domain']
		self.imgs_path = marry_var['path']
		self.wget = wget()
		self.db = MySql()
		proxy_host = '61.7.186.5:52552'
		userpass = 'vpn:vpn'
		self.wget.set_proxy(proxy_host)

	def guess(self):
		url_pre = self.domain + '/htm_data/16/1711/'
		start_num = 2790477
		end_num = 270000

		for num in range(start_num,end_num,-1):
			ful_url = url_pre + str(num) +'.html'
			print self.wget.get_content(ful_url)
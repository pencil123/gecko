#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import yaml

class config():
	config_path = "config/config.yaml"
	def __init__(self,config=""):
		self.config_path = config if config else self.config_path
		self.parse()

	def parse(self):
		config_handler = open(self.config_path)
		config_info = yaml.load(config_handler)
		self.marry = config_info['marry']
		self.mysql = config_info['mysql']
		self.proxy = config_info['proxy']
		self.discuz = config_info['discuz']
		

handler = config()
marry_var = handler.marry
mysql_var = handler.mysql
proxy_var = handler.proxy
discuz_var = handler.discuz
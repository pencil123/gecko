#!/usr/bin/env python2.7
# -*- encoding: utf-8; py-indent-offset: 4 -*-

import gearman
import time
from utils import connect
class raw_content():
	def __init__(self):
		self.client = gearman.GearmanClient(['localhost:4730'])
		self.admin = gearman.GearmanAdminClient(['localhost:4730'])
		self.job_list = []
		self.conn,self.cursor = connect()
	def submit_jobs(self,data_sting):
		job_request = self.client.submit_job("raw_content",data_sting,background=True)#,
		self.job_list.append(job_request)

	def control(self):
		for num100 in range(14202):
			sql_string = 'select id,url from url where status=0 limit %s,100' % (100*num100)
			self.cursor.execute(sql_string)
			count_tuple = self.cursor.fetchall()
			for num in range(len(count_tuple)):
				string = '-'.join(str(e) for e in count_tuple[num])
				self.submit_jobs(string)

handler = raw_content()
handler.control()
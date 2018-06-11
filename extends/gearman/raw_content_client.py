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
		self.db = MysqlConn()
	def submit_jobs(self,data_sting):
		job_request = self.client.submit_job("raw_content",data_sting,background=True)#,
		self.job_list.append(job_request)
	# def check_jobs_status(self,job):
		
	# 	#print self.admin.get_workers()
	# 	#print self.client.get_job_status(job)
	# 	if job.state == 'COMPLETE':
	# 		print "Job %s finished!  Result: %s - %s" % (job.job.unique, job.state, job.result)
	# 		self.job_list.remove(job)

	def control(self):
		for num100 in range(31541):
			sql = 'select pagedate,pagenum from guess where pagenum<2938810 order by id asc limit %s,100' % (100*num100)
			pagenum_tuple = self.db.selectall(sql)
			for num in range(len(pagenum_tuple)):
				string = '-'.join(str(e) for e in pagenum_tuple[num])
				self.submit_jobs(string)
		# 		pagedate,pagenum = pagenum_tuple[num]
		# 		self.url_page(pagedate,pagenum)
		# 		print pagedate,pagenum



		# num = 1
		# while num < 100:
		# 	print 'num: ',num
		# 	print self.admin.get_status()
		# 	status = self.admin.get_status()[0]['queued']
		# 	print 'queued: ',status
		# 	if status < 10:
		# 		self.submit_jobs('job data' + str(num))
		# 		num = num +1
			# for job_num in range(len(self.job_list)):
			# 	self.check_jobs_status(self.job_list[job_num])
			#time.sleep(1)

handler = gm_clients()
handler.control()

# print 'hello'
# check_request_status(completed_job_request)
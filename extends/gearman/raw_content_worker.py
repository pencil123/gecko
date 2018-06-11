#!/usr/bin/env python2.7
# -*- encoding: utf-8; py-indent-offset: 4 -*-
import gearman
import time
import re
from bs4 import BeautifulSoup as BS

from raw_content import raw_content
from utils import connect


gm_worker = gearman.GearmanWorker(['localhost:4730'])

# def task_listener_reverse(gearman_worker, gearman_job):
#   time.sleep(1)
#   print 'Reversing string: ' + gearman_job.data
#   return gearman_job.data[::-1]

class raw_content(object):
    def __init__(self):
        self.conn,self.cursor = connect()
        self.pattern=re.compile(r'https://t66y.com/htm_data/(\d+)/(\d+)/(\d+)\.html',re.DOTALL)

    def update_db(self,gearman_worker, gearman_job):
        data_list = gearman_job.data.split('-')
        col_id = int(data_list[0])
        url = int(data_list[1])
        
        match = self.pattern.match(url)
        url_id,url_date,url_num = match.groups()

        thread_dict = {}
        thread_dict['fid'] = url_id
        thread_dict['thread_url'] = url

        count_sql = "select count(*) from raw_content where url='%s'" % (url,)
        self.cursor.execute(count_sql)
        count_tuple = self.cursor.fetchall()
        if count_tuple[0][0]:
            return 'False'

        if self.raw_content.download(**thread_dict):
                update_sql = "update url set status=1 where id= %s" % (col_id)
                self.cursor.execute(update_sql)

        return 'True'

handler = raw_content()
# gm_worker.set_client_id is optional
gm_worker.set_client_id('worker')
gm_worker.register_task('raw_content', handler.update_db)

# Enter our work loop and call gm_worker.after_poll() after each time we timeout/see socket activity
gm_worker.work()
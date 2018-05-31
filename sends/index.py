#! /usr/bin/env python
# -*- coding: utf-8 -*-
from discuz.discuz import DiscuzAPI
from libs.mysqlconn import MysqlConn

db = MysqlConn()


handler = DiscuzAPI('http://umt365.com')
handler.login('admin','123Grey')

sql = 'select title,content from pages where fid=15 order by id asc'
results = db.selectall(sql)
for num in range(len(results)):
    subject,msg = results[num]
    handler.publish(42,subject,msg)

sql = 'select title,content from pages where fid=4 order by id asc'
results = db.selectall(sql)
for num in range(len(results)):
    subject,msg = results[num]
    handler.publish(43,subject,msg)

sql = 'select title,content from pages where fid=5 order by id asc'
results = db.selectall(sql)
for num in range(len(results)):
    subject,msg = results[num]
    handler.publish(44,subject,msg)

sql = 'select title,content from pages where fid=25 order by id asc'
results = db.selectall(sql)
for num in range(len(results)):
    subject,msg = results[num]
    handler.publish(45,subject,msg)

sql = 'select title,content from pages where fid=26 order by id asc'
results = db.selectall(sql)
for num in range(len(results)):
    subject,msg = results[num]
    handler.publish(46,subject,msg)

sql = 'select title,content from pages where fid=27 order by id asc'
results = db.selectall(sql)
for num in range(len(results)):
    subject,msg = results[num]
    handler.publish(47,subject,msg)

sql = 'select title,content from pages where fid=21 order by id asc'
results = db.selectall(sql)
for num in range(len(results)):
    subject,msg = results[num]
    handler.publish(48,subject,msg)

sql = 'select title,content from pages where fid=22 order by id asc'
results = db.selectall(sql)
for num in range(len(results)):
    subject,msg = results[num]
    handler.publish(49,subject,msg)
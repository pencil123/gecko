#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import cookielib
import random
import string
import re
import time
import sys
import httplib
import mimetools
import mimetypes

httplib.HTTPConnection.debuglevel = 1

class DiscuzAPI:
	def __init__(self, forumUrl):
		''' 初始化论坛url代理服务器 '''
		self.forumUrl = forumUrl
		self.formhash = ''
		self.isSign = False
		self.xq = ''
		self.jar = cookielib.CookieJar()
		openner = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.jar))
		urllib2.install_opener(openner)
 
	def login(self,username=u'',password=u''):
		''' 登录论坛 '''
		url = self.forumUrl + "/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&inajax=1";

		postData = urllib.urlencode({'username': username.encode('utf-8'),
		'password': password.encode('utf-8'),
		'answer': '', 'cookietime': '2592000', 'handlekey': 'ls', 'questionid': '0',
		'quickforward': 'yes',  'fastloginfield': 'username'})

		req = urllib2.Request(url,postData)
		content = urllib2.urlopen(req).read()
		if username.encode('utf-8') in content:
			if self.get_formhash():
				print 'logon success!'
			return 1
		else:
			print 'logon faild!'
			return 0

	def logout(self):
		url = self.forumUrl + "/member.php?mod=logging&action=logout&formhash=" + self.formhash
		urllib2.urlopen(url).read()

	def get_formhash(self):
		url = self.forumUrl + "/forum.php"
		content = urllib2.urlopen(url).read().decode('utf-8')
		rows = re.findall(r'<input type=\"hidden\" name=\"formhash\" value=\"(.*?)\" />', content)
		if len(rows)!=0:
			self.formhash = rows[0]
			return True
		else:
			return False


	def register(self,username=u'',password=u'',email=u'',fields={}):
		url = self.forumUrl + "/member.php?mod=register"
		content = urllib2.urlopen(url).read().decode('utf-8')
		rows = re.findall(r'<input type=\"hidden\" name=\"formhash\" value=\"(.*?)\" />', content)
		if len(rows)!=0:
			self.formhash = rows[0]
			print 'formhash is: ' + self.formhash
		else:
			print 'none formhash!'

		url = self.forumUrl + "/member.php?mod=register&inajax=1"
		data_post = urllib.urlencode({'formhash':self.formhash,
		fields['username']:username.encode('utf-8'),
		fields['password']:password.encode('utf-8'),
		fields['password1']:password.encode('utf-8'),
		fields['email']:email.encode('utf-8'),
		'regsubmit':'yes',
		'referer':'http://bbs.gudcloud.com/forum.php',
		'activationauth':''})
		req = urllib2.Request(url,data_post)
		content = urllib2.urlopen(req).read().decode('utf-8')
		if username in content:
			return True
		else:
			return False

	def reply(self, tid, subject = u'',msg = u'支持~~'):
		''' 回帖 '''
		url = self.forumUrl + '/forum.php?mod=post&action=reply&fid=41&tid='+str(tid)+'&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1'
		postData = urllib.urlencode({'formhash': self.formhash, 'message': msg.encode('utf-8'), 'subject': subject.encode('utf-8'), 'posttime':int(time.time()) })
		req = urllib2.Request(url,postData)
		content = urllib2.urlopen(req).read().decode('utf-8')
		#print content
		if u'发布成功' in content:
			print 'reply success!'
		else:
			print 'reply faild!'

	def publish(self,fid,subject=u'主题',msg=u'内容',imgId = "",attachId = ""):
		'''发帖'''
		print subject,msg
		url = self.forumUrl + '/forum.php?mod=post&action=newthread&fid=' + str(fid) + '&topicsubmit=yes&infloat=yes&handlekey=fastnewpost&inajax=1'
		refer = self.forumUrl + "/forum.php?mod=forumdisplay&fid=%d" % fid
		postData = urllib.urlencode(
			{'formhash':self.formhash,
			'message':msg.encode('utf-8'),
			'subject':subject.encode('utf-8'),
			'posttime':int(time.time()),
			#'addfeed':'1', 
			#'allownoticeauthor':'1', 
			#'checkbox':'0', 
			#'newalbum':'', 
			#'readperm':'', 
			#'rewardfloor':'', 
			#'rushreplyfrom':'', 
			#'rushreplyto':'', 
			#'save':'', 
			#'stopfloor':'', 
			#'typeid':typeid,
			#'attachnew[%s][description]' % imgId: "",
			#'attachnew[%s][description]' % attachId: "",
			#'uploadalbum':'', 
			'usesig':'1', 
			'wysiwyg':'0'})
		print postData
		req = urllib2.Request(url,postData)
		req.add_header('Referer',refer)
		content = urllib2.urlopen(req).read().decode('utf-8')
		print content
		if u"您的主题已发布" in content:
			print 'publish success!'
			return 1
		else:
			print 'publish faild!'
			print content
			exit()
			return 0

		

	def uploadImage(self,imageData, fid=48,imgname="default.jpg",imgtype="jpg"):
		imageId = None
		#上传图片

		url = self.forumUrl + "/forum.php?mod=post&action=newthread&fid=%d&extra=" % fid
		data = urllib2.urlopen(url).read().decode('utf-8')

		pattern = re.compile(r'hash\":\"(.*?)\"',re.M)
		hash_list = pattern.findall(data)
		print hash_list
		# Upload the image
		uploadImageUrl = self.forumUrl + "/misc.php?mod=swfupload&operation=upload&simple=1&type=image"
		refer = self.forumUrl + "/forum.php?mod=post&action=newthread&fid=%d&extra=" % fid
		randomStr = "7dd" + ''.join( random.sample(string.ascii_lowercase + string.digits, 8) )
		CRLF = '\r\n'
		#BOUNDARY = mimetools.choose_boundary()
		BOUNDARY = "---------------------------" + randomStr
		L = []
		L.append('--' + BOUNDARY)
		L.append("Content-Disposition: form-data; name=\"uid\""  )
		L.append("")
		L.append("2")
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name=\"hash\"')
		L.append("")
		L.append(hash_list[0])
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name=\"Filedata\"; filename=\"' + imgname + '\"')
		L.append("Content-Type: image/" + imgtype)
		L.append("")
		L.append( imageData )
		L.append('--' + BOUNDARY + '--')
		L.append("")
		postData = CRLF.join(str(a) for a in L)
		#print postData

		req = urllib2.Request(uploadImageUrl, postData) 
		req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % BOUNDARY )
		req.add_header('Content-Length',  len(postData) )
		req.add_header('Referer', refer )
		resp = urllib2.urlopen(req)
		body = resp.read().decode('utf-8')
		bodySp = body.split('|')
		if len(bodySp) == 0:
			return None
		if bodySp[0] == u'DISCUZUPLOAD' and bodySp[1] == u'0':
			imageId = bodySp[2]
		return imageId

	def uploadAttach(self,imageData, fid=48,btname="default.torrent"):
		imageId = None
		# 上传附件

		url = self.forumUrl + "/forum.php?mod=post&action=newthread&fid=%d&extra=" % fid
		data = urllib2.urlopen(url).read().decode('utf-8')

		pattern = re.compile(r'hash\":\"(.*?)\"',re.M)
		hash_list = pattern.findall(data)
		print hash_list
		# Upload the image
		uploadImageUrl = self.forumUrl + "/misc.php?mod=swfupload&operation=upload&simple=1"
		refer = self.forumUrl + "/forum.php?mod=post&action=newthread&fid=%d&extra=" % fid
		randomStr = "7dd" + ''.join( random.sample(string.ascii_lowercase + string.digits, 8) )
		CRLF = '\r\n'
		#BOUNDARY = mimetools.choose_boundary()
		BOUNDARY = "---------------------------" + randomStr
		L = []
		L.append('--' + BOUNDARY)
		L.append("Content-Disposition: form-data; name=\"uid\""  )
		L.append("")
		L.append("2")
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name=\"hash\"')
		L.append("")
		L.append(hash_list[0])
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name=\"Filedata\"; filename=\"' + btname + '\"')
		L.append("Content-Type: application/torrent")
		L.append("")
		L.append( imageData )
		L.append('--' + BOUNDARY + '--')
		L.append("")
		postData = CRLF.join(str(a) for a in L)

		req = urllib2.Request(uploadImageUrl, postData) 
		req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % BOUNDARY )
		req.add_header('Content-Length',  len(postData) )
		req.add_header('Referer', refer )
		resp = urllib2.urlopen(req)
		body = resp.read().decode('utf-8')
		print body
		bodySp = body.split('|')
		if len(bodySp) == 0:
			return None
		if bodySp[0] == u'DISCUZUPLOAD' and bodySp[1] == u'0':
			imageId = bodySp[2]
		return imageId


# def ed2k(ed2k_infos):
# 	try:
# 		info_json = eval(ed2k_infos)
# 	except:
# 		return ""
# 	info_str = ""
# 	for m in range(len(info_json)):
# 		name = info_json[m]['fileNameed2k']
# 		size = info_json[m]['size_ed2k']
# 		ed2k = info_json[m]['ed2k'].replace("\\","")
# 		qqdl = info_json[m]['qqdl'].replace("\\","")
# 		thunder = info_json[m]['thunder'].replace("\\","")

# 		info_str = info_str + "[b]" + name +"  "+ size + "[/b]\n" + "ed2k下载：[code]" + ed2k + "[/code]\nQQ旋风下载：[code]" + qqdl + "[/code]\n迅雷下载：[code]" +thunder + "[/code]\n"
# 	return info_str
# if __name__ == '__main__':
# 	mdb = mysqldb()
# 	sql_str = "select id,url,name,content,image,btfilename,bbsfid,ed2k from infos where status =1"
# 	info_list = mdb.selectall(sql_str)
# 	robot = DiscuzAPI("http://bbs.gudcloud.com")
# 	robot.login("jacky","helloworld")
# 	for m in range(len(info_list)):
# 		update_id =  info_list[m][0]
# 		print update_id
# 		subject = info_list[m][2]
# 		message = info_list[m][3]
# 		file_img = "/www/boma/python/ck180/" + info_list[m][4]

# 		fid = info_list[m][6]
# 		img_type = file_img.split('.')[-1]
# 		img_name = subject + "." + img_type
# 		img_name=img_name.replace('/','-')
# 		imageData = open(file_img, 'rb').read()
# 		imgId = robot.uploadImage(imageData,fid,imgname=img_name,imgtype=img_type)

# 		btname = subject + ".torrent"
# 		btname=btname.replace('/','-')
# 		print btname
# 		attachId = ""
# 		if info_list[m][5]:
# 			file_bt = "/www/boma/python/ck180/" + info_list[m][5]
# 			fileData = open(file_bt,'rb').read()
# 			attachId = robot.uploadAttach(fileData,fid,btname=btname)
# 		else:
# 			attachId = ""
# 			message = message+ed2k(info_list[m][7])
# 		robot.publish(fid,subject=subject,msg=message,imgId=imgId,attachId=attachId)
# 		sql_str = "update infos set status =2 where id=%s" % (update_id)
# 		mdb.query(sql_str)
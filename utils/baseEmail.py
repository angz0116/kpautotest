
# -*- coding:utf-8 -*-
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import threading
import utils.readConfig as readConfig
from utils.baseLog import MyLog
import zipfile
import glob

Config = readConfig.ReadConfig()

class Email:
	def __init__(self):
		global host, user, password, port, sender, title, content
		host = Config.get_email("mail_host")
		user = Config.get_email("mail_user")
		password = Config.get_email("mail_pass")
		port = Config.get_email("mail_port")
		sender = Config.get_email("sender")
		title = Config.get_email("subject")
		content = Config.get_email("content")
		self.value = Config.get_email("receiver")
		self.receiver = []
		for n in str(self.value).split("/"):
			self.receiver.append(n)
		date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		self.subject = title + " " + date
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.msg = MIMEMultipart('mixed') #related,alternative

	def config_header(self):
		self.msg['subject'] = self.subject
		self.msg['from'] = sender
		self.msg['to'] = ";".join(self.receiver)

	def config_content(self):
		content_plain = MIMEText(content, 'plain', 'utf-8')  #html超文本
		self.msg.attach(content_plain)

	def config_file(self):
		if self.check_file():
			reportpath = self.log.get_result_path()
			#zippath = os.path.join(reportpath, "test.zip")
			# zip file
			files = glob.glob(reportpath + '\*')
			#f = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
			#for file in files:
			#    f.write(file)
			#f.close()
#添加附件1
			with open(files[1], 'rb') as reportfile:
				filehtml = MIMEText(reportfile.read(), 'base64', 'utf-8')
				filehtml.add_header('Content-Disposition', 'attachment', filename="测试报告.html")
				filehtml.add_header('Content-ID', '<0>')
				filehtml.add_header('X-Attachment-Id', '0')
				filehtml.add_header('Content-Type', 'application/octet-stream')
				self.msg.attach(filehtml)
#添加附件2
			with open(files[0], 'rb') as logfile:
				filelog = MIMEText(logfile.read(), 'base64', 'utf-8')
				filelog.add_header('Content-Disposition', 'attachment', filename="测试日志.txt")
				filelog.add_header('Content-ID', '<0>')
				filelog.add_header('X-Attachment-Id', '0')
				filelog.add_header('Content-Type', 'application/octet-stream')
				self.msg.attach(filelog)

	def check_file(self):
		reportpath = self.log.get_report_path()
		if os.path.isfile(reportpath) and not os.stat(reportpath) == 0:
			return True
		else:
			return False

	def send_email(self):
		self.config_header()
		self.config_content()
		self.config_file()
		try:
			smtp = smtplib.SMTP()
			smtp.connect(host)
			smtp.login(user, password)
			smtp.sendmail(sender, self.receiver, self.msg.as_string())
			smtp.quit()
			self.logger.info("测试报告已发送邮件")
		except Exception as ex:
			self.logger.error(str(ex))

class MyEmail:
	email = None
	mutex = threading.Lock()

	def __init__(self):
		pass

	@staticmethod
	def get_email():

		if MyEmail.email is None:
			MyEmail.mutex.acquire()
			MyEmail.email = Email()
			MyEmail.mutex.release()
		return MyEmail.email


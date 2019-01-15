# -*- coding:utf-8 -*-
import requests
import utils.readConfig as readConfig
from utils.baseLog import MyLog as Log
import json

Config = readConfig.ReadConfig()

class ConfigHttp:
	def __init__(self):
		self.httpname = None
		self.log = Log.get_log()
		self.logger = self.log.logger
		self.headers = {}
		self.params = {}
		self.data = {}
		self.url = None
		self.files = {}
		self.moduletype = None
	#接口时用该url
	def set_url(self, url):
		host = Config.get_http(self.httpname, "url")
		if self.httpname == "LCJC1":
			if self.moduletype == "CT":
				port = "10059"
			elif self.moduletype == "AC":
				port = "10039"
			elif self.moduletype == "WP":
				port = "10079"
			elif self.moduletype == "BI":
				port = "10049"
			elif self.moduletype == "MK":
				port = "10029"
			elif self.moduletype == "MS":
				port = "10069"
		else:
			port = Config.get_http(self.httpname, "port")
		self.url = host + ":" + port + url
	'''
	#打开页面需要用该url
	def set_url(self, url):
		host = Config.get_http(self.httpname, "url")
		port = Config.get_http(self.httpname, "port")
		self.url = host + ":" + port + url
	'''

	def set_headers(self, header):
		self.headers = header

	def set_params(self, param):
		self.params = param

	def set_data(self, data):
		self.data = data

	def set_files(self, file):
		self.files = file

	def post(self):
		timeout = Config.get_http(self.httpname, "timeout")
		try:
			response = requests.post(self.url, headers=self.headers, data=json.dumps(self.data), files=self.files, timeout=float(timeout))
			res = json.loads(response.content)
			return res
		except requests.exceptions.ReadTimeout:
			self.logger.error("发送接口请求超时，请修改timeout时间")
			return None

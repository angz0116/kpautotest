# -*- coding:utf-8 -*-
import requests
import utils.readConfig as readConfig
from utils.baseLog import MyLog as Log
import json
import hashlib

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
		#port = Config.get_http(self.httpname, "port")
		#self.url = host + ":" + port + url
		self.url = host + url
		print(self.url)

	def set_headers(self):
		self.headers = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}

	def set_params(self, param):
		self.params = param

	def set_data(self, data):
		self.data = data

	def set_files(self, file):
		self.files = file

	def post(self):
		timeout = Config.get_http(self.httpname, "timeout")
		try: #json格式时json.dumps(self.data)，form表单的是self.data
			response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files, timeout=float(timeout))
			res = json.loads(response.content)
			return res
		except requests.exceptions.ReadTimeout:
			self.logger.error("发送接口请求超时，请修改timeout时间")
			return None

	def getyz(self,url):
		#timeout = Config.get_http(self.httpname, "timheaders=self.headers,eout")
		try: #json格式时json.dumps(self.data)，form表单的是self.data
			response = requests.get(url, headers=self.headers, params=self.data)
			res = json.loads(response.content)
			return res
		except requests.exceptions.ReadTimeout:
			self.logger.error("发送接口请求超时，请修改timeout时间")
			return None

	def get(self):
		timeout = Config.get_http(self.httpname, "timeout")
		try: #json格式时json.dumps(self.data)，form表单的是self.data
			response = requests.get(self.url, headers=self.headers, params=self.data, timeout=float(timeout))
			if response.content:
				res = json.loads(response.content)
				return res
			else:
				return None
		except requests.exceptions.ReadTimeout:
			self.logger.error("发送接口请求超时，请修改timeout时间")
			return None

	def md5utils(self,paramdic, url):
		secretkey = "PC3937!@*&YZF"
		urldict = {"url": url}
		newparams = dict(paramdic, **urldict)
		sorted(newparams.items(), key=lambda item: item[0], reverse=True)
		strparams = ""
		i = 0
		for key, value in newparams.items():
			if (i > 0):
				strparams += "&"
			strparams += key
			strparams += "="
			strparams += value
			i += 1
		strparams += "&serchay=" + secretkey
		hl = hashlib.md5()
		hl.update(strparams.encode(encoding='utf-8'))
		t = hl.hexdigest()
		h2 = hashlib.md5()
		h2.update(t.encode(encoding='utf-8'))
		return h2.hexdigest()


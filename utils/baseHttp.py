# -*- coding:utf-8 -*-
import requests
import utils.readConfig as readConfig
from utils.baseLog import MyLog as Log
import json
import hashlib
import operator

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
		self.secretkey = None

	#接口时用该url
	def set_url(self, url, paramdic, token):
		host = Config.get_http(self.httpname, "url")
		self.secretkey = Config.get_http(self.httpname, "secretkey")
		if token == "":
			self.urldict = {"path": url}
		else:
			self.urldict = {"path": url, "token": token}
		self.newparams = dict(paramdic, **self.urldict)
		# 得到拼接参数后，进行升序排列reverse=Flase默认是升序，True时是降序
		self.sortparams = sorted(self.newparams.items(), key=lambda x: x[0])
		# 升序后把每个参数都拼接在一起，进行md5双重加密
		self.strparams = ""
		i = 0
		for key, value in self.sortparams:
			if (i > 0):
				self.strparams += "&"
			self.strparams += key
			self.strparams += "="
			self.strparams += value
			i += 1
		self.strparams += "&secretkey=" + self.secretkey
		# md5加密，双重加密
		hl = hashlib.md5()
		hl.update(self.strparams.encode(encoding='utf-8'))
		fristmd5 = hl.hexdigest()
		h2 = hashlib.md5()
		h2.update(fristmd5.encode(encoding='utf-8'))
		# 获取到md5加密后的sn
		self.sn = h2.hexdigest()
		if token == "":
			self.urlq = url + "?sn=" + self.sn
		else:
			self.urlq = url + "?sn=" + self.sn + "&token=" + token
		self.url = host + self.urlq
		#print(self.url)

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

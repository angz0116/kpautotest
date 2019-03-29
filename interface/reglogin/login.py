# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
from datadao.verifyCode import getVerifyCode
interfaceNo = "login"
name = "用户登录"

req = ConfigHttp()
sqldb = ConfigDB()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 登录(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 测试用例,url, mobile,logintype, password, token, 预期结果):
		self.No = str(No)
		self.url = str(url)
		self.mobile = str(mobile)
		self.logintype = str(logintype)
		self.password = str(password)
		self.token = str(token)

	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		print(interfaceNo + name + "CASE " + self.No)

	"""用户登录"""
	def test_body(self):
		req.httpname = "KPTEST"
		self.url = get_excel("url", self.No, interfaceNo)
		# 手机号
		self.mobile = get_excel("mobile", self.No, interfaceNo)
		# 登录凭证类型 1=短信验证码  2=密码登录
		self.logintype = get_excel("logintype", self.No, interfaceNo)
		if self.logintype =="1":
			self.password = getVerifyCode(self.No, "register", self.mobile)
		else:
			self.password = get_excel("password", self.No, "login")
		print("用户登录接口__login手机号==" + str(self.mobile))
		self.data = {
			"username": self.mobile,
			"password": self.password,
			"login_type": self.logintype,
			"app_version": "8.0.0",
			"system": "3",
			"device_model": "HUAWEI P10",
			"system_version": "V1.0.0",
			"country_code": "86",
			"channel": "5"
		}

		req.set_url(self.url)
		req.set_data(self.data)
		self.response = req.post()
		try:
			self.retcode = self.response["code"]
		except Exception:
			self.logger.error("报文返回为空！")
			print("报文返回为空！")
		self.check_result()
		self.wr_excel()

	def check_result(self):
		try:
			self.assertEqual(self.retcode, 0, self.logger.info("检查是否登录成功"))
			if self.retcode==0:
				tokenp = self.response["data"]["token"]
				set_excel(tokenp, "token", self.No, interfaceNo)
			set_excel("pass", "测试结果", self.No, interfaceNo)
			self.logger.info("测试通过")
		except AssertionError:
			set_excel("fail", "测试结果", self.No, interfaceNo)
			self.msg = self.response["msg"]
			self.logger.error("测试失败")
		self.msg = self.response["msg"]
		self.logger.info(self.msg)
	# 写入xls文件中
	def wr_excel(self):
		set_excel(self.data, "请求报文", self.No, interfaceNo)
		set_excel(self.response, "返回报文", self.No, interfaceNo)
		set_excel(self.msg,"预期结果",self.No, interfaceNo)
		set_excel(self.password, "password", self.No, interfaceNo)

	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_case_line("预期结果", self.msg)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)
if __name__ == '__main__':
	unittest.main()


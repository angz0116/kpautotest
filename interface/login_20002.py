# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime
interfaceNo = "20002"
name = "登录接口20002"

req = ConfigHttp()
sqldb = ConfigDB()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class test_login20002(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, responseBody, mobile):
		self.No = str(No)
		self.mobile = str(mobile)
	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		print(interfaceNo + name + "CASE " + self.No)

	def test_body(self):
		self.url = "/wmsystem/service/" + interfaceNo + "/v1"
		headers = {"Content-Type": "application/json"}
		# 手机号
		self.mobile = get_excel("mobile", self.No, "20001")
		# 获取当前时间
		now = datetime.datetime.now()
		# 请求流水号
		self.transNo = now.strftime('%Y%m%d') + str(random.randint(0, 90000000))
		# 请求
		self.transTime = now.strftime('%Y-%m-%d %H:%M:%S')
		print("登录接口__20002手机号==" + str(self.mobile))
		self.data = {
			"interfaceNo": interfaceNo,
			"isGesture": "0",
			"mobile": self.mobile,
			"loginPwd": "YG5qde1DVnZnSHmFFyQTWw==",
			"sysSource": "5",
			"transNo": self.transNo,
			"transTime": self.transTime
		}
		req.httpname = "LCJC3"
		req.set_url(self.url)
		req.set_headers(headers)
		req.set_data(self.data)
		self.response = req.post()
		try:
			self.retcode = self.response["responseBody"]["retCode"]
			#返回报文
			self.responsebody = self.response["responseBody"]
		except Exception:
			self.logger.error("报文返回为空！")
			print("报文返回为空！")

		self.check_result()
		self.wr_excel()

	def check_result(self):
		try:
			self.assertEqual(self.retcode, "0000", self.logger.info("检查是否登录成功"))
			set_excel("pass", "测试结果", self.No, interfaceNo)
			self.logger.info("测试通过")
		except AssertionError:
			set_excel("fail", "测试结果", self.No, interfaceNo)
			errorDesc = self.response["errorDesc"]
			self.logger.error("测试失败:"+errorDesc)
	# 写入xls文件中
	def wr_excel(self):
		set_excel(self.data, "请求报文", self.No, interfaceNo)
		set_excel(self.response, "返回报文", self.No, interfaceNo)
		set_excel(self.responsebody, "responseBody", self.No, interfaceNo)
		set_excel(self.mobile, "mobile", self.No, interfaceNo)

	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_case_line("responsebody", self.responsebody)
		#self.log.build_case_line("返回SQL", self.res)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
	unittest.main()


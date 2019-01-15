# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime,time
from service.gainHtml import savehtml,openaccount
interfaceNo = "20003"
name = "设置密码接口20003"

req = ConfigHttp()
sqldb = ConfigDB()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class test_setpwd20003(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 查询SQL, mobile):
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
		# 证件号码
		self.cardNo = get_excel("cardNo", self.No, "20005")
		# 获取当前时间
		now = datetime.datetime.now()
		# 请求流水号
		self.transNo = now.strftime('%Y%m%d') + str(random.randint(0, 90000000))
		# 请求
		self.transTime = now.strftime('%Y-%m-%d %H:%M:%S')
		print("设置密码接口__20003手机号==" + str(self.mobile))
		self.data = {
			"interfaceNo": interfaceNo,
			"cardType": "1",
			"cardNo": self.cardNo,
			"mobile": self.mobile,
			"newPwd": "YG5qde1DVnZnSHmFFyQTWw==",
			"transPwd": "YG5qde1DVnZnSHmFFyQTWw==",
			"biztype": "05",  # 01：重置登录密码；02：修改登录密码；03：重置交易密码;04：修改交易密码;05：设置交易密码;
			"sysSource": "5",
			"transNo": self.transNo,
			"transTime": self.transTime
		}
		req.httpname = "LCJC3"
		req.set_url(self.url)
		req.set_headers(headers)
		req.set_data(self.data)
		self.response = req.post()
		print(self.data)
		try:
			self.retcode = self.response["responseBody"]["retCode"]
		except Exception:
			self.logger.error("报文返回为空！")
			print("报文返回为空！")

		self.check_result()
		self.wr_excel()

	def check_result(self):
		try:
			self.assertEqual(self.retcode, "0000", self.logger.info("检查是否设置密码成功"))
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
		#set_excel(self.SQL, "查询SQL", self.No, interfaceNo)
		set_excel(self.mobile, "mobile", self.No, interfaceNo)

	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		#self.log.build_case_line("查询SQL", self.SQL)
		#self.log.build_case_line("返回SQL", self.res)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
	unittest.main()


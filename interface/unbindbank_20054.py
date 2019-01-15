# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime,time

interfaceNo = "20054"
name = "存管解绑接口20054"

req = ConfigHttp()
sqldb = ConfigDB()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class test_unbindbank20054(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, responsebody ,custCode):
		self.No = str(No)
		self.custCode = str(custCode)


	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		print(interfaceNo + name + "CASE " + self.No)

	def test_body(self):
		self.url = "/wmsystem/service/" + interfaceNo + "/v1"
		headers = {"Content-Type": "application/json"}
		# 客户编号
		self.custCode = get_excel("custCode", self.No, "20053")
		# 银行卡号
		self.bankAcctNo = get_excel("bankAcctNo", self.No, "20053")
		# 获取当前时间
		now = datetime.datetime.now()
		# 流水号
		self.transNo = now.strftime('%Y%m%d') + str(random.randint(0, 90000000))
		# 请求流水号
		self.bindcardSid = str(random.randint(0, 2000000)) + "" + str(round(time.time() * 1000))  # 毫秒级时间戳
		# 请求时间
		self.transTime = now.strftime("%Y-%m-%d %H:%M:%S")
		print("存管解绑__20054接口&&==客户编号：" + self.custCode+"&&银行卡号："+self.bankAcctNo)
		self.data = {
			"interfaceNo": interfaceNo,
			"custCode": self.custCode,
			"bankAcctNo": self.bankAcctNo,
			"bindCardSid": self.bindcardSid,
			"callPageUrl": "http://www.baidu.com",
			"trustChannelCode": "02",
			"sysSource": "5",
			"isAppFlg": "1",
			"isTrust": "2",
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
			# 获取返回报文
			self.responsebody = self.response["responseBody"]
		except Exception:
			self.errorDesc = self.response["errorDesc"]
			self.logger.error("报文返回为空！失败原因："+self.errorDesc)
			print("报文返回为空！失败原因："+self.errorDesc)

		self.check_result()
		self.wr_excel()

	def check_result(self):
		try:
			self.assertEqual(self.retcode, "0000", self.logger.info("检查是否存管解绑成功"))
			set_excel("pass", "测试结果", self.No, interfaceNo)
			self.logger.info("测试通过，请求流水号："+self.bindcardSid)
		except AssertionError:
			set_excel("fail", "测试结果", self.No, interfaceNo)
			errorDesc = self.response["errorDesc"]
			self.logger.error("测试失败,失败原因:"+errorDesc)

	# 写入xls文件中
	def wr_excel(self):
		set_excel(self.data, "请求报文", self.No, interfaceNo)
		set_excel(self.response, "返回报文", self.No, interfaceNo)
		set_excel(self.custCode, "custCode", self.No, interfaceNo)
		set_excel(self.responsebody, "responsebody", self.No, interfaceNo)

	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
	unittest.main()


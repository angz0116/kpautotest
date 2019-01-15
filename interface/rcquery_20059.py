# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime,time
from service.gainHtml import savehtml,openrecharge

interfaceNo = "20059"
name = "充值查询接口20059"

req = ConfigHttp()
sqldb = ConfigDB()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class test_rcquery20059(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 查询SQL,custCode, bankAcctNo, amount,status):
		self.No = str(No)
		self.custCode = str(custCode)
		self.bankAcctNo = str(bankAcctNo)
		self.amount = str(amount)
		self.status = str(status)
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
		self.depositSid = str(random.randint(0, 2000000)) + "" + str(round(time.time() * 1000))  # 毫秒级时间戳
		# 请求时间
		self.transTime = now.strftime("%Y-%m-%d %H:%M:%S")
		print("充值查询__20059接口&&==客户编号：" + self.custCode + "&&==银行卡号：" + self.bankAcctNo)
		self.data = {
			"interfaceNo": interfaceNo,
			"custCode": self.custCode,
			"depositSid": self.depositSid,
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
		print(self.response)
		try:
			self.retcode = self.response["responseBody"]["retCode"]
			# 获取金额
			self.amount = self.response["responseBody"]["amount"]
			# 获取充值结果
			self.status = self.response["responseBody"]["status"]
		except Exception:
			self.errorDesc = self.response["errorDesc"]
			self.logger.error("报文返回为空！失败原因："+self.errorDesc)
			print("报文返回为空！失败原因："+self.errorDesc)

		self.check_result()
		self.wr_excel()

	def check_result(self):
		try:
			self.assertEqual(self.retcode, "0000", self.logger.info("检查是否绑定银行卡成功"))
			set_excel("pass", "测试结果", self.No, interfaceNo)
			self.logger.info("测试通过，请求流水号："+self.depositSid)
		except AssertionError:
			set_excel("fail", "测试结果", self.No, interfaceNo)
			errorDesc = self.response["errorDesc"]
			self.logger.error("测试失败,失败原因:"+errorDesc)

	# 写入xls文件中
	def wr_excel(self):
		set_excel(self.data, "请求报文", self.No, interfaceNo)
		set_excel(self.response, "返回报文", self.No, interfaceNo)
		set_excel(self.custCode, "custCode", self.No, interfaceNo)
		set_excel(self.bankAcctNo, "bankAcctNo", self.No, interfaceNo)
		set_excel(self.amount, "amount", self.No, interfaceNo)
		set_excel(self.status, "status", self.No, interfaceNo)

	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
	unittest.main()


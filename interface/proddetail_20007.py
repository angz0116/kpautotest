# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime
interfaceNo = "20007"
name = "理财产品详情接口20007"

req = ConfigHttp()
sqldb = ConfigDB()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class test_proddetail20007(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 查询SQL):
		self.No = str(No)

	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		print(interfaceNo + name + "CASE " + self.No)

	def test_body(self):
		self.url = "/wmsystem/service/" + interfaceNo + "/v1"
		headers = {"Content-Type": "application/json"}
		# 客户编号
		self.ecifId = get_excel("custCode", self.No, "20053")
		# 理财产品代码
		self.productCode = get_excel("productCode", self.No, "20042")
		# 理财计划编号
		self.planNo = get_excel("planNo", self.No, "20042")
		# 版本号
		self.productVersion = get_excel("productVersion", self.No, "20042")
		# 获取当前时间
		now = datetime.datetime.now()
		# 流水号
		self.transNo = now.strftime('%Y%m%d') + str(random.randint(0, 90000000))
		# 请求时间
		self.transTime = now.strftime("%Y-%m-%d %H:%M:%S")
		self.data = {
			"interfaceNo": interfaceNo,
			"productCode": self.productCode,
			"productVersion": self.productVersion,
			"planNo": self.planNo,
			"type": "2",#1.查询理财产品，2.查询理财计划
			"ecifId": self.ecifId,
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
			self.responsebody = self.response["responseBody"]
		except Exception:
			self.logger.error("报文返回为空！")
			print("报文返回为空！")

		#self.check_sql()
		self.check_result()
		self.wr_excel()

	def check_result(self):
		try:
			self.assertEqual(self.retcode, "0000", self.logger.info("检查是否理财产品详情成功"))
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
		set_excel(self.responsebody, "responsebody", self.No, interfaceNo)
		'''
		set_excel(self.customerID, "customerID", self.No, interfaceNo)
		set_excel(self.investNum, "investNum", self.No, interfaceNo)
		set_excel(self.investAmount, "investAmount", self.No, interfaceNo)
		set_excel(self.investDate, "investDate", self.No, interfaceNo)
		set_excel(self.expireDate, "expireDate", self.No, interfaceNo)
		set_excel(self.depository, "depository", self.No, interfaceNo)
		set_excel(self.transuccesstime, "transuccesstime", self.No, interfaceNo)
		'''


	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		#self.log.build_case_line("查询SQL", self.SQL)
		#self.log.build_case_line("返回SQL", self.res)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
	unittest.main()


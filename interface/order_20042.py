# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime
interfaceNo = "20042"
name = "在线下订单接口20042"

req = ConfigHttp()
sqldb = ConfigDB()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class test_order20042(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 查询SQL, productCode, productName, planNo, planName, yieldRate, productVersion):
		self.No = str(No)
		self.productCode = str(productCode)
		self.productName = str(productName)
		self.planNo = str(planNo)
		self.planName = str(planName)
		self.yieldRate = float(yieldRate)
		self.productVersion = int(productVersion)

	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		print(interfaceNo + name + "CASE " + self.No)

	def test_body(self):
		self.url = "/wmsystem/service/" + interfaceNo + "/v1"
		headers = {"Content-Type": "application/json"}
		# 手机号
		self.mobile = get_excel("bankMobile", self.No, "20053")
		# 客户编号
		self.ecifId = get_excel("custCode", self.No, "20053")
		# 客户姓名
		self.custName = get_excel("bankAcctName", self.No, "20053")
		# 优惠券编号
		self.couponSn = get_excel("couponSn", self.No, "20053")
		# 理财产品代码
		self.productCode = get_excel("productCode", self.No, interfaceNo)
		# 理财产品名称
		self.productName = get_excel("productName", self.No, interfaceNo)
		# 理财计划编号
		self.planNo = get_excel("planNo", self.No, interfaceNo)
		# 理财计划名称
		self.planName = get_excel("planName", self.No, interfaceNo)
		# 收益
		self.yieldRate = get_excel("yieldRate", self.No, interfaceNo)
		# 版本号
		self.productVersion = get_excel("productVersion", self.No, interfaceNo)
		# 获取当前时间
		now = datetime.datetime.now()
		# 流水号
		self.transNo = now.strftime('%Y%m%d') + str(random.randint(0, 90000000))
		# 请求时间
		self.transTime = now.strftime("%Y-%m-%d %H:%M:%S")
		print("在线下订单__20042接口&&==客户编号：" + self.ecifId + "&&==理财计划编号：" + self.planNo + "&&==理财计划名称：" + self.planName)
		self.data = {
			"interfaceNo": interfaceNo,
			"orderType": "1",
			"investMode": "2",
			"payAmount": "800000",
			"investAmount": "800000",
			"mobile": self.mobile,
			"custName": self.custName,
			"ecifId": self.ecifId,
			"productCode": self.productCode,
			"productName": self.productName,
			"planNo": self.planNo,
			"planName": self.planName,
			"productVersion": self.productVersion,
			"yieldRate": self.yieldRate,
			"payType": "0",
			"sysSource": "5",
			"couponUse": "0",
			#"couponList":[{"couponAmt": "8",
			#"couponSn": self.couponSn,
			#"couponType": "3"}],
			"transNo": self.transNo,
			"transTime": self.transTime
		}
		req.httpname = "LCJC4"
		req.set_url(self.url)
		req.set_headers(headers)
		req.set_data(self.data)
		self.response = req.post()
		try:
			self.retcode = self.response["responseBody"]["retCode"]
			#获取订单编号
			self.orderNo = self.response["responseBody"]["orderNo"]
		except Exception:
			self.logger.error("报文返回为空！")
			print("报文返回为空！")

		self.check_result()
		self.wr_excel()

	def check_result(self):
		try:
			self.assertEqual(self.retcode, "0000", self.logger.info("检查是否在线下订单成功"))
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
		set_excel(self.orderNo, "orderNo", self.No, "20025")

	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		#self.log.build_case_line("查询SQL", self.SQL)
		#self.log.build_case_line("返回SQL", self.res)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
	unittest.main()


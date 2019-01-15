# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime
interfaceNo = "20025"
name = "理财购买接口20025"

req = ConfigHttp()
sqldb = ConfigDB()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class test_buylc20025(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 查询SQL, orderNo, customerID , investNum, investAmount, investDate, expireDate, depository, transuccesstime):
		self.No = str(No)
		self.orderNo = str(orderNo)
		self.customerID = str(customerID)
		self.investNum = str(investNum)
		self.investAmount = str(investAmount)
		self.investDate = str(investDate)
		self.expireDate = str(expireDate)
		self.depository = str(depository)
		self.transuccesstime = str(transuccesstime)
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
		# 客户ID
		self.customerID = get_excel("customerID", self.No, "20053")
		# 订单编号
		self.orderNo = get_excel("orderNo", self.No, interfaceNo)
		# 获取当前时间
		now = datetime.datetime.now()
		# 流水号
		self.transNo = now.strftime('%Y%m%d') + str(random.randint(0, 90000000))
		# 请求时间
		self.transTime = now.strftime("%Y-%m-%d %H:%M:%S")
		print("理财购买__20025接口&&==客户编号：" + self.ecifId + "&&==手机号：" + self.mobile)
		self.data = {
			"interfaceNo": interfaceNo,
			"orderNo": self.orderNo,
			"ecifId": self.ecifId,
			"mobile": self.mobile,
			"freePwd": "2",
			"sysSource": "5",
			"transPwd": "YG5qde1DVnZnSHmFFyQTWw==",
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
		except Exception:
			self.logger.error("报文返回为空！")
			print("报文返回为空！")

		self.check_sql()
		self.check_result()
		self.wr_excel()

	def check_result(self):
		try:
			self.assertEqual(self.retcode, "0000", self.logger.info("检查是否理财购买成功"))
			set_excel("pass", "测试结果", self.No, interfaceNo)
			self.logger.info("测试通过")
		except AssertionError:
			set_excel("fail", "测试结果", self.No, interfaceNo)
			errorDesc = self.response["errorDesc"]
			self.logger.error("测试失败:"+errorDesc)

		# 检验sql是否插入数据库中
	def check_sql(self):
		sqldb.dbname = "LC4DB"
		self.SQL = get_sql("LCDB", "wm_t_invest_info", "customerID") % self.customerID
		cursor = sqldb.executeSQL(self.SQL)
		try:
			self.res = sqldb.get_one(cursor)
			# 出借编号
			self.investNum = self.res[0]
			# 出借金额
			self.investAmount = self.res[1]
			# 出借日期
			self.investDate = self.res[2]
			# 到期日期
			self.expireDate = self.res[3]
			# 存管机构
			self.depository = self.res[4]
			# 交易成功
			self.transuccesstime = self.res[5]
		except Exception:
			print("SQL查询结果为空！")
			self.logger.exception("SQL查询结果为空！")
		sqldb.closeDB()

	# 写入xls文件中
	def wr_excel(self):
		set_excel(self.data, "请求报文", self.No, interfaceNo)
		set_excel(self.response, "返回报文", self.No, interfaceNo)
		set_excel(self.SQL, "查询SQL", self.No, interfaceNo)
		set_excel(self.customerID, "customerID", self.No, interfaceNo)
		set_excel(self.investNum, "investNum", self.No, interfaceNo)
		set_excel(self.investAmount, "investAmount", self.No, interfaceNo)
		set_excel(self.investDate, "investDate", self.No, interfaceNo)
		set_excel(self.expireDate, "expireDate", self.No, interfaceNo)
		set_excel(self.depository, "depository", self.No, interfaceNo)
		set_excel(self.transuccesstime, "transuccesstime", self.No, interfaceNo)

	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_case_line("查询SQL", self.SQL)
		self.log.build_case_line("返回SQL", self.res)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
	unittest.main()


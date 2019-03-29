# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime,time
from service.districtcode import gennerator
from service.gainName import getFullName

interfaceNo = "20005"
name = "实名认证接口20005"

req = ConfigHttp()
sqldb = ConfigDB()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class test_cel20005(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 查询SQL, cardNo, custName, custCode, customerID):
		self.No = str(No)
		self.cardNo = str(cardNo)
		self.custName = str(custName)
		self.custCode = str(custCode)
		self.customerID = str(customerID)
	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		print(interfaceNo + name + "CASE " + self.No)

	def test_body(self):
		req.httpname = "LCJC3"
		# 客户信息模块
		req.moduletype = "CT"
		if req.httpname == "LCJC1" :
			self.url = "/customer/CT004/v2"
		else:
			self.url = "/wmsystem/service/" + interfaceNo + "/v1"
		headers = {"Content-Type": "application/json"}
		# 生成身份证号
		self.cardNo = gennerator()
		# 获取客户姓名
		self.custName = getFullName()
		# 获取20001接口中的mobile
		self.mobile = get_excel("mobile", self.No, "20001")
		# 获取当前时间
		now = datetime.datetime.now()
		# 请求流水号
		transNo = now.strftime('%Y%m%d') + str(random.randint(0, 90000000))
		# 请求
		transTime = now.strftime('%Y-%m-%d %H:%M:%S')
		# 开户流水
		openAccountSid = str(random.randint(0, 2000000)) + "" + str(round(time.time() * 1000))  # 毫秒级时间戳
		print("实名认证__20005接口**==" + "手机号：" + self.mobile + "**==身份证号：" + self.cardNo)
		self.data = {
			"interfaceNo": interfaceNo,
			"mobile": self.mobile,
			"cardNo": self.cardNo,
			"custName": self.custName,
			"managerUserId": "10017212",
			#理财人开户信息
			"trustChannelCode": "02",
			"isTrust": "2",  # (1,非存管;2,存管)
			"isAppFlg": "1",
			"openAccountSid": openAccountSid,
			"isOpenInwardAccount": "01",
			"sysSource": "5",
			"transTime": transTime,
			"transNo": transNo
		}
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
			self.assertEqual(self.retcode, "0000", self.logger.info("检查是否实名认证成功"))
			set_excel("pass", "测试结果", self.No, interfaceNo)
			self.logger.info("测试通过")
		except AssertionError:
			set_excel("fail", "测试结果", self.No, interfaceNo)
			self.logger.error("测试失败")

	# 检验sql是否插入数据库中
	def check_sql(self):
		sqldb.dbname = "LC3DB"
		self.SQL = get_sql("LCDB", "WM_T_USER_REG", "identify_number") % self.cardNo
		cursor = sqldb.executeSQL(self.SQL)
		try:
			self.res = sqldb.get_one(cursor)
			if self.res is None:
				print("该客户未实名")
			else:
				self.custCode = str(self.res[16])
				self.customerID = str(self.res[17])
		except Exception:
			print("SQL查询结果为空！")
			self.logger.exception("SQL查询结果为空！")
		sqldb.closeDB()

	# 写入xls文件中
	def wr_excel(self):
		set_excel(self.data, "请求报文", self.No, interfaceNo)
		set_excel(self.response, "返回报文", self.No, interfaceNo)
		set_excel(self.SQL, "查询SQL", self.No, interfaceNo)
		set_excel(self.cardNo, "cardNo", self.No, interfaceNo)
		set_excel(self.custName, "custName", self.No, interfaceNo)
		set_excel(self.custCode, "custCode", self.No, interfaceNo)
		set_excel(self.customerID, "customerID", self.No, interfaceNo)
		#set_excel(self.custCode, "custCode", self.No, "20051")
		#set_excel(self.mobile, "mobile", self.No, "20051")

	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_case_line("查询SQL", self.SQL)
		self.log.build_case_line("返回SQL", self.res)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
	unittest.main()


# -*- coding:utf-8 -*-
from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime,time
from service.gainHtml import savehtml, opencheckpwd
interfaceNo = "20110"
name = "存管客户验证交易密码"

req = ConfigHttp()
sqldb = ConfigDB()

@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class test_checkpwd20110(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 查询SQL, custCode):
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
		# 从excle中获取客户编号
		self.custCode = get_excel("custCode", self.No, interfaceNo)
		# 获取订单号
		self.orderNo = get_excel("orderNo", self.No, "20025")
		# 获取当前时间
		now = datetime.datetime.now()
		# 请求流水号
		transNo = now.strftime('%Y%m%d') + str(random.randint(0, 90000000))
		# 请求流水号
		payPasswordSid = str(random.randint(0, 2000000)) + "" + str(round(time.time() * 1000))  # 毫秒级时间戳
		# 请求
		transTime = now.strftime("%Y-%m-%d %H:%M:%S")
		print("存管客户验证交易密码__20110接口&&==手机号：" + self.mobile + "&&==客户编号：" + self.ecifId)
		self.data = {
			"interfaceNo": interfaceNo,
			"custCode": self.custCode,
			"orderNo":self.orderNo,
			"payPasswordSid": payPasswordSid,
			"callPageUrl": "http://www.baidu.com",
			"sysSource": "5",
			"transNo": transNo,
			"transTime": transTime
		}
		req.httpname = "LCJC3"
		req.set_url(self.url)
		req.set_headers(headers)
		req.set_data(self.data)
		self.response = req.post()
		try:
			self.retcode = self.response["responseBody"]["retCode"]
			# 从返回报文中截取html文本
			htmlContext = self.response["responseBody"]["htmlContext"]
			# 把获取的html文本保存到程html文件
			savehtml("checkpwd", htmlContext, self.No)
			# 打开存管客户验证交易密码
			opencheckpwd("checkpwd", self.No , self.mobile)
		except Exception:
			self.logger.error("报文返回为空！")
			print("报文返回为空！")

		self.check_sql()
		self.check_result()
		self.wr_excel()

	def check_result(self):
		try:
			self.assertEqual(self.retcode, "0000", self.logger.info("存管客户验证交易密码是否成功"))
			set_excel("pass", "测试结果", self.No, interfaceNo)
			self.logger.info("测试通过")
		except AssertionError:
			set_excel("fail", "测试结果", self.No, interfaceNo)
			errorDesc = self.response["errorDesc"]
			self.logger.error("测试失败:" + errorDesc)

	# 检验sql是否插入数据库中
	def check_sql(self):
		sqldb.dbname = "LC3DB"
		self.SQL = get_sql("LCDB", "wm_t_customer_info", "custCode") % self.ecifId
		cursor = sqldb.executeSQL(self.SQL)
		try:
			self.res = sqldb.get_one(cursor)
			self.customerID = str(self.res[0])
		except Exception:
			print("SQL查询结果为空！")
			self.logger.exception("SQL查询结果为空！")
		sqldb.closeDB()

	# 写入xls文件中
	def wr_excel(self):
		set_excel(self.data, "请求报文", self.No, interfaceNo)
		set_excel(self.response, "返回报文", self.No, interfaceNo)
		set_excel(self.SQL, "查询SQL", self.No, interfaceNo)
		#set_excel(self.customerID, "customerID", self.No, interfaceNo)

	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_case_line("查询SQL", self.SQL)
		self.log.build_case_line("返回SQL", self.res)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
	unittest.main()
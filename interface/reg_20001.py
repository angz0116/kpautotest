# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime
from service.gainPhone import createPhone

interfaceNo = "20001"
name = "注册接口20001"

req = ConfigHttp()
sqldb = ConfigDB()

@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class test_reg20001(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 查询SQL, mobile):
		self.No = str(No)
		self.mobile = str(mobile)

	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		print(interfaceNo + name + "CASE " + self.No)

	def test_body(self):
		req.httpname = "LCJC3"
		#客户信息模块
		req.moduletype = "CT"
		if req.httpname == "LCJC1" :
			self.url = "/customer/CT001/v2"
		else:
			self.url = "/wmsystem/service/" + interfaceNo + "/v1"
		headers = {"Content-Type": "application/json"}
		#获取手机号
		if self.No == "10":
			telphone = "18211014910"
		else:
			telphone = "1821101491"+str((int(self.No)))

		#telphone = createPhone()

		# 获取当前时间
		now = datetime.datetime.now()
		# 请求流水号
		transNo = now.strftime('%Y%m%d') + str(random.randint(0, 90000000))
		# 请求
		transTime = now.strftime('%Y-%m-%d %H:%M:%S')
		print("注册接口__20001手机号==" + telphone)
		self.data = {
			"interfaceNo": interfaceNo,
			"loginPwd": "YG5qde1DVnZnSHmFFyQTWw==",
			"mobile": telphone,
			"userNo": "10017212",
			"sysSource": "5",
			"transNo": transNo,
			"transTime": transTime
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
		self.check_sql(telphone)
		self.check_result()
		self.wr_excel(telphone)
	
	def check_result(self):
		try:
			self.assertEqual(self.retcode, "0000", self.logger.info("检查是否注册成功"))
			set_excel("pass", "测试结果", self.No, interfaceNo)
			self.logger.info("测试通过")
		except AssertionError:
			set_excel("fail", "测试结果", self.No, interfaceNo)
			self.logger.error("测试失败")
	# 检验sql是否插入数据库中
	def check_sql(self, tmobile):
		sqldb.dbname = "LC3DB"
		self.SQL = get_sql("LCDB", "WM_T_USER_REG", "mobile") %tmobile
		cursor = sqldb.executeSQL(self.SQL)
		try:
			self.res = sqldb.get_one(cursor)
			self.resql = float(self.res[0])
		except Exception:
			print("SQL查询结果为空！")
			self.logger.exception("SQL查询结果为空！")
		sqldb.closeDB()
	# 写入xls文件中
	def wr_excel(self,tmobile):
		set_excel(self.data, "请求报文", self.No, interfaceNo)
		set_excel(self.response, "返回报文", self.No, interfaceNo)
		set_excel(self.SQL, "查询SQL", self.No, interfaceNo)
		set_excel(tmobile, "mobile", self.No, interfaceNo)
	
	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_case_line("查询SQL", self.SQL)
		self.log.build_case_line("返回SQL", self.res)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)

if __name__ =='__main__':
	unittest.main()


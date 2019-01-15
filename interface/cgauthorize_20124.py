# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime,time
from service.gainHtml import savehtml,openauthorize
interfaceNo = "20124"
name = "存管客户授权申请20124"

req = ConfigHttp()
sqldb = ConfigDB()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class test_cgauthorize20124(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 查询SQL, custCode, jyacctId, dpacctId, reqbusiparam):
		self.No = str(No)
		self.ecifId = str(custCode)
		self.jyacctId = str(jyacctId)
		self.dpacctId = str(dpacctId)
		self.reqbusiparam = str(reqbusiparam)
	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		print(interfaceNo + name + "CASE " + self.No)

	def test_body(self):
		self.url = "/wmsystem/service/" + interfaceNo + "/v1"
		headers = {"Content-Type": "application/json"}
		# 客户编号
		self.ecifId = get_excel("custCode", self.No, "20005")
		# 获取当前时间
		now = datetime.datetime.now()
		# 流水号
		self.transNo = now.strftime('%Y%m%d') + str(random.randint(0, 90000000))
		# 请求流水号
		self.reqId = str(random.randint(0, 2000000)) + "" + str(round(time.time() * 1000))  # 毫秒级时间戳
		# 请求时间
		self.transTime = now.strftime("%Y-%m-%d %H:%M:%S")
		print("存管客户授权申请__20124接口&&==客户编号：" + self.ecifId)
		self.data = {
			"interfaceNo": interfaceNo,
			"ecifId": self.ecifId,
			"reqId": self.reqId,
			# 前端回调地址
			"callPageUrl": "http://172.18.100.93:8081/depository/resultAuthorization/v1",
			# 存管机构
			"dpChannel": "02",
			# 业务类型标识 1:贷款 2:理财
			"isLoanFlg": "2",
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
			# 从返回报文中截取html文本
			htmlContext = self.response["responseBody"]["htmlContext"]
			# 把获取的html文本保存到程html文件
			savehtml("authorize", htmlContext, self.No)
			# 打开授权管理页面
			openauthorize("authorize", self.No)
			# 获取请求流水号
			self.depositsid = self.response["responseBody"]["depositSid"]
		except Exception:
			self.errorDesc = self.response["errorDesc"]
			self.logger.error("报文返回为空！失败原因："+self.errorDesc)
			print("报文返回为空！失败原因："+self.errorDesc)

		self.check_sql()
		self.check_result()
		self.wr_excel()

	def check_result(self):
		try:
			self.assertEqual(self.retcode, "0000", self.logger.info("检查是否授权成功"))
			set_excel("pass", "测试结果", self.No, interfaceNo)
			#self.logger.info("测试通过，请求流水号："+self.depositsid)
		except AssertionError:
			set_excel("fail", "测试结果", self.No, interfaceNo)
			errorDesc = self.response["errorDesc"]
			self.logger.error("测试失败,失败原因:"+errorDesc)

	# 检验sql是否插入数据库中
	def check_sql(self):

		sqldb.dbname = "CORE3DB"
		self.SQL = get_sql("COREDB", "t_c_dp_cust_oper", "custCode") % self.ecifId
		cursor = sqldb.executeSQL(self.SQL)
		try:
			self.res = sqldb.get_one(cursor)
			# 内部户
			self.jyacctId = self.res[0]
			# 存管户
			self.dpacctId = self.res[1]
			# 业务系统请求参数
			self.reqbusiparam = self.res[2]
		except Exception:
			print("SQL查询结果为空！")
			self.logger.exception("SQL查询结果为空！")
		sqldb.closeDB()


	# 写入xls文件中
	def wr_excel(self):
		set_excel(self.data, "请求报文", self.No, interfaceNo)
		set_excel(self.response, "返回报文", self.No, interfaceNo)
		set_excel(self.SQL, "查询SQL", self.No, interfaceNo)
		set_excel(self.ecifId, "custCode", self.No, interfaceNo)
		set_excel(self.jyacctId,"jyacctId",self.No , interfaceNo)
		set_excel(self.dpacctId, "dpacctId", self.No, interfaceNo)
		set_excel(self.reqbusiparam, "reqbusiparam", self.No, interfaceNo)

	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_case_line("查询SQL", self.SQL)
		self.log.build_case_line("返回SQL", self.res)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
	unittest.main()


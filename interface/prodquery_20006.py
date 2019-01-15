# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime
interfaceNo = "20006"
name = "理财产品查询接口20006"

req = ConfigHttp()
sqldb = ConfigDB()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class test_prodquery20006(unittest.TestCase):
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
		# 获取当前时间
		now = datetime.datetime.now()
		# 流水号
		self.transNo = now.strftime('%Y%m%d') + str(random.randint(0, 90000000))
		# 请求时间
		self.transTime = now.strftime("%Y-%m-%d %H:%M:%S")
		self.data = {
			"interfaceNo": interfaceNo,
			"type": "2",#1.查询理财产品，2.查询理财计划
			"channel": "5",#1.store,2.app，3.web,5.向前app，6.向前web，7.向前微信
			"currentPage": "1",
			"pageSize": "3",
			"trustType": "2",#1：非存管;2：存管
			"depository": "02",#非存管:00(捷越);存管:01(华瑞);(02)恒丰
			"sysSource": "5",
			"orderType": "3",#1.按封闭期；2.按预期收益率;3."抢购中"状态的产品,按产品上线时间倒序由上至下显示;“已售罄”状态产品 按产品出借完成时间倒序由上至下显示;4.大家都在投;5.发售时间
			"sortType": "2",#1.升序;2.降序
			"planStatus":"03", #00：已上线；01：已下线；02：已满标处理；03：发售中；04：已撤销；05：已发布；
			"transNo": self.transNo,
			"transTime": self.transTime
		}
		req.httpname = "LCJC1"
		req.set_url(self.url)
		req.set_headers(headers)
		req.set_data(self.data)
		self.response = req.post()
		try:
			self.retcode = self.response["responseBody"]["retCode"]
			self.planList = self.response["responseBody"]["planList"]
		except Exception:
			self.logger.error("报文返回为空！")
			print("报文返回为空！")

		#self.check_sql()
		self.check_result()
		self.wr_excel()

	def check_result(self):
		try:
			self.assertEqual(self.retcode, "0000", self.logger.info("检查是否理财产品查询成功"))
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
		# set_excel(self.SQL, "查询SQL", self.No, interfaceNo)
		if len(self.planList)>0:
			i=int(self.No)-1
			plans = self.planList[i]
			# 写入在线购买order20042接口
			set_excel(plans["planNo"], "planNo", self.No, "20042")
			set_excel(plans["planName"], "planName", self.No, "20042")
			set_excel(plans["productCode"], "productCode", self.No, "20042")
			set_excel(plans["productName"], "productName", self.No, "20042")
			set_excel(plans["productRate"], "yieldRate", self.No, "20042")
			set_excel(plans["productVersion"], "productVersion", self.No, "20042")
	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		#self.log.build_case_line("查询SQL", self.SQL)
		#self.log.build_case_line("返回SQL", self.res)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
	unittest.main()


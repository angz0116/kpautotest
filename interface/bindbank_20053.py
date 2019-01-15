# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime
from service.gainHtml import savehtml,openbindBank
from service.gainBank import getbankCode,getCMBbankCardNo,getCCBbankCardNo
interfaceNo = "20053"
name = "绑定银行卡接口20053"

req = ConfigHttp()
sqldb = ConfigDB()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class test_bindbank20053(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 查询SQL,customerID, custCode, cardNo, bankMobile, bankAcctNo, bankAcctName, bankCode, couponSn):
		self.No = str(No)
		self.custCode = str(custCode)
		self.customerID = str(customerID)
		self.cardNo = str(cardNo)
		self.bankMobile = str(bankMobile)
		self.bankAcctNo = str(bankAcctNo)
		self.bankAcctName = str(bankAcctName)
		self.bankCode = str(bankCode)
		self.couponSn = str(couponSn)

	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		print(interfaceNo + name + "CASE " + self.No)

	def test_body(self):
		req.httpname = "LCJC3"
		req.moduletype = "AC"
		if req.httpname == "LCJC1" :
			self.url = "/account/AC004/v2"
		else:
			self.url = "/wmsystem/service/" + interfaceNo + "/v1"
		headers = {"Content-Type": "application/json"}
		# 获取客户编号
		self.custCode = get_excel("custCode", self.No, "20005")
		# 获取身份证号
		self.cardNo = get_excel("cardNo", self.No, "20005")
		# 获取银行卡号
		self.bankAcctNo = getCCBbankCardNo()
		# 根据银行卡号，获取银行代码
		self.bankCode = getbankCode(self.bankAcctNo)
		# 假如得到的银行代码为空，则重新生成招商
		if (self.bankCode == "" and len(self.bankCode) == 0):
			# 重新获取招商银行卡号
			self.bankAcctNo = getCMBbankCardNo()
			# 获取银行代码号
			self.bankCode = getbankCode(self.bankAcctNo)
		# 获取客户姓名
		self.bankAcctName = get_excel("custName", self.No, "20005")
		# 获取预留手机号
		self.mobile = get_excel("mobile", self.No, "20001")
		# 获取客户ID
		self.customerID = get_excel("customerID", self.No, "20005")
		# 获取当前时间
		now = datetime.datetime.now()
		# 请求流水号
		self.transNo = now.strftime('%Y%m%d') + str(random.randint(0, 90000000))
		# 绑定银行流水号
		self.bindCardSid = now.strftime('%Y%m%d') + str(random.randint(0, 20000000))
		# 请求
		self.transTime = now.strftime('%Y-%m-%d %H:%M:%S')
		self.data = {
			"interfaceNo": interfaceNo,
			"bankMobile": self.mobile,
			"custCode": self.custCode,
			"bankAcctNo": self.bankAcctNo,
			"bankAcctName": self.bankAcctName,
			"callPageUrl": "http://www.baidu.com",
			"bindCardSid": self.bindCardSid,
			"bankCode": self.bankCode,
			#"bankId": self.bankCode,
			"trustChannelCode": "02",
			"sysSource": "5",
			"isTrust": "2",
			"isAppFlg": "1",
			"transNo": self.transNo,
			"transTime": self.transTime
		}
		req.set_url(self.url)
		req.set_headers(headers)
		req.set_data(self.data)
		self.response = req.post()
		print("绑定银行卡__20053接口**==" + "手机号：" + self.mobile + "**==客户编号：" + self.custCode + "**==银行卡号：" + self.bankAcctNo + "**==银行代码：" + self.bankCode)
		try:
			self.retcode = self.response["responseBody"]["retCode"]
			# 从返回报文中截取html文本
			htmlContext = self.response["responseBody"]["htmlContext"]
			# 把获取的html文本保存到程html文件
			savehtml("bindBank", htmlContext, self.No)
			# 打开绑定银行页面
			openbindBank("bindBank", self.No)
		except Exception:
			self.errorDesc = self.response["errorDesc"]
			self.logger.error("报文返回为空！失败原因："+self.errorDesc)
			print("报文返回为空！失败原因："+self.errorDesc)

		self.check_sql()
		self.check_result()
		self.wr_excel()

	def check_result(self):
		try:
			self.assertEqual(self.retcode, "0000", self.logger.info("检查是否绑定银行卡成功"))
			set_excel("pass", "测试结果", self.No, interfaceNo)
			self.logger.info("测试通过")
		except AssertionError:
			set_excel("fail", "测试结果", self.No, interfaceNo)
			errorDesc = self.response["errorDesc"]
			self.logger.error("测试失败:"+errorDesc)

	# 检验sql是否插入数据库中
	def check_sql(self):
		sqldb.dbname = "LC3DB"
		self.SQL = get_sql("LCDB", "wm_t_bank_info", "customerID") % self.customerID
		cursor = sqldb.executeSQL(self.SQL)
		try:
			self.res = sqldb.get_one(cursor)
			#bindtxt = str(self.res[17])
		except Exception:
			print("SQL查询结果为空！")
			self.logger.exception("SQL查询结果为空！")
		sqldb.closeDB()

	# 写入xls文件中
	def wr_excel(self):
		set_excel(self.data, "请求报文", self.No, interfaceNo)
		set_excel(self.response, "返回报文", self.No, interfaceNo)
		set_excel(self.SQL, "查询SQL", self.No, interfaceNo)
		set_excel(self.custCode, "custCode", self.No, interfaceNo)
		set_excel(self.customerID, "customerID", self.No, interfaceNo)
		set_excel(self.cardNo, "cardNo", self.No, interfaceNo)
		set_excel(self.mobile, "bankMobile", self.No, interfaceNo)
		set_excel(self.bankAcctName, "bankAcctName", self.No, interfaceNo)
		set_excel(self.bankAcctNo, "bankAcctNo", self.No, interfaceNo)
		set_excel(self.bankCode, "bankCode", self.No, interfaceNo)

	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_case_line("查询SQL", self.SQL)
		self.log.build_case_line("返回SQL", self.res)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)

if __name__ == '__main__':
	unittest.main()


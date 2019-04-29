# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import time
from service.gainPhone import createPhone
from service.gainName import getFullName
from datadao.sendverify import getSendverify
from datadao.queryverify import query_sql
interfaceNo = "register"
name = "用户注册"

req = ConfigHttp()
sqldb = ConfigDB()

@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 注册(unittest.TestCase):
	"""注册已存在的用户"""

	def setParameters(self, No, 测试结果, 测试用例, 请求报文, 返回报文,url, mobile, regtype, countrycode, verifycode,password, flag, 预期结果):
		self.No = str(No)
		self.url = str(url)
		self.mobile = str(mobile)
		self.regtype = str(regtype)
		self.countrycode = str(countrycode)
		self.verifycode = str(verifycode)
		self.password = str(password)
		self.flag = str(flag)

	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		self.tcase = get_excel("测试用例", self.No, interfaceNo)
		print(interfaceNo + name + "CASE " + self.No)


	def test_body(self):
		"""
		self.tcase
		"""
		req.httpname = "KPTEST"
		self.logger.info(self.tcase)
		self.url = get_excel("url", self.No, interfaceNo)
		# flag为1时，则重新生成新手机号；flag为2时，则从excel中读取已存在的
		self.flag = get_excel("flag", self.No, interfaceNo)
		# 根据flag进行判断，手机号是否生成新手机号
		if(self.flag=="1"):
			# 重新生成新手机号
			self.telphone = createPhone()
		else:
			# 从excel中获取手机号
			self.telphone = get_excel("mobile", self.No, interfaceNo)
		# 获取姓名
		self.nick = getFullName()
		# 注册密码
		self.password = get_excel("password", self.No, interfaceNo)
		# 注册类型 1=普通密码注册 2=短信验证码
		self.regtype = get_excel("regtype", self.No, interfaceNo)
		# 国家编码，86中国，其他国外
		self.countrycode = get_excel("countrycode", self.No, interfaceNo)
		# 获取验证码的方法
		self.veresult = getSendverify(self.logger, "reg", "mobile", self.telphone, self.countrycode)
		if self.veresult ==0:
			time.sleep(10)
			# 从数据库中查询验证码
			self.verifycode = query_sql(self.logger,self.telphone,self.countrycode)
		# 根据注册类型判断是输入验证码或密码
		print("用户注册接口手机号==" + self.telphone)
		self.data = {
			"mobile": self.telphone,
			"nick": self.nick,
			"reg_type": self.regtype,
			"verify": self.verifycode,
			"pass": self.password,
			"source": "1",
			"country_code": self.countrycode,
			"yk_token": "5",
			"app_version": "8.0.0",
			"system": "3",
			"device_model": "HUAWEI P10",
			"system_version": "V1.0.0",
			"channel": "5"
		}
		#print(self.data)
		req.set_url(self.url, self.data, token="")
		req.set_data(self.data)
		self.response = req.post()
		try:
			print(self.response)
			self.retcode = self.response["code"]
		except Exception:
			self.logger.error("报文返回为空！")
			print("报文返回为空！")
		self.check_result()
		self.wr_excel()
	
	def check_result(self):
		try:
			self.assertEqual(self.retcode, "0", self.logger.info("检查是否注册成功"))
			set_excel("pass", "测试结果", self.No, interfaceNo)
			self.logger.info("测试通过")
		except AssertionError:
			set_excel("fail", "测试结果", self.No, interfaceNo)
			self.logger.error("测试失败")
		self.msg = self.response["msg"]
		self.logger.info(self.msg)
	# 写入xls文件中
	def wr_excel(self):
		'''
        set_excel(r'"'+str(self.data)+'"', "请求报文", self.No, interfaceNo)
        set_excel(r'"'+str(self.response)+'"', "返回报文", self.No, interfaceNo)
        '''
		set_excel(self.telphone, "mobile", self.No, interfaceNo)
		set_excel(self.msg, "预期结果", self.No, interfaceNo)
		set_excel(self.verifycode,"verifycode", self.No, interfaceNo)
		# 注册成功后，则把手机号写入“检查是否注册”的接口中
		set_excel(self.telphone, "mobile", self.No, "getMobileStatus")
		set_excel(self.countrycode, "countrycode", self.No, "login")
	
	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_case_line("预期结果", self.msg)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)
if __name__ =='__main__':
	unittest.main()



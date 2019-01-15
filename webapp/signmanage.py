# -*- coding:utf-8 -*-
from utils.baseBrowser import BaseBrowser
from webapp.comlogin import test_comLogin
from selenium.webdriver.support.select import Select
from utils.baseDB import ConfigDB
from utils.baseUtils import *
import time,unittest ,datetime
from service.myglobal import get_value
from utils.baseLog import MyLog as Log
log = Log.get_log()
logger = log.logger
#数据库连接信息
sqldb = ConfigDB()
'''
第六步，签约管理-签约管理菜单，admin，管理员
'''
class test_signmanage(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		# 必须使用@classmethod 装饰器,所有test运行前运行一次
		#time.sleep(300)
		# 得到driver实例
		self.driver = BaseBrowser.getDriver()
		logger.info("第六步************************signmanage.py，签约管理-签约管理，amdin，管理员")
	'''
	打开签约管理-签约管理菜单及页面
	'''
	def openmenu(self):
		# 进入“信审系统”,与哪个环境
		httpname = "LOANJC5"
		systemname = "credit"
		# 用信审专员登录
		test_comLogin.test_login(self.driver, "11043892", "Cs654321", httpname, systemname)
		time.sleep(3)
		#关闭第一个菜单“贷后监控”
		self.driver.find_element_by_id("firstMenu0").click()
		#打开“签约管理”菜单
		self.driver.find_element_by_id("firstMenu8").click()
		#打开“签约管理-签约管理”页面
		self.driver.find_element_by_xpath("//span[text()=' 签约管理']").click()
		#进入该“签约管理”页面的iframe
		self.driver.find_element_by_xpath("//iframe[contains(@src,'toQueryPage')]")
		time.sleep(3)
	'''
	生成合同
	'''
	def test_makecontract(self):
		try:
			# 进件编号
			#intoappId = get_value()
			intoappId = "120154558491"
			logger.info("通过第一步进件申请，得到进件编号：" + intoappId)
			auditestate = self.check_sql(intoappId)
			# 进件状态等于5100待签约时，可以点生成合同等其他操作
			if auditestate == "5100":
				# 调用"打开菜单"的方法
				self.openmenu()
				# 录入“进件编号”
				self.driver.find_element_by_name("intoAppId").send_keys(intoappId)
				# 点“查询”按钮
				self.driver.find_element_by_xpath("//span[text()='查询']").click()
				time.sleep(3)
				# 点击生成合同按钮，及进行其他操作
				# 点击“单选按钮”，选中该进件信息
				self.driver.find_element_by_xpath("//input[type='radio']").click()
				# 点击“生成合同”按钮
				self.driver.find_element_by_link_text("生成合同").click()
				# 预约放款日期
				planLoansDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				self.driver.find_element_by_id("dtoplanLoansDate").send_keys(planLoansDate)
				# 点“保存”按钮，提交生成合同
				self.driver.find_element_by_xpath("//div[@class='ui-dialog-buttonset']/button[1]/span").click()
				#调用“合同下载”方法
				self.contractdown()
			else:#否则就是进件信息还未到待签约
				logger.info("该进件信息未在待签约")
		except Exception as err:
			logger.info("第六步，签约管理-签约管理,生成合同错误信息：")
			logger.error(err)
	'''
	合同下载
	'''
	def contractdown(self):
		try:
			time.sleep(3)
			# 点击“单选按钮”，选中该进件信息
			self.driver.find_element_by_xpath("//input[type='radio']").click()
			# 点击“合同下载”按钮
			self.driver.find_element_by_link_text("合同下载").click()
			# 点击“PC电子签章”按钮，提示“签章完成”则正确
			self.driver.find_element_by_xpath("//span[text()='PC电子签章']").click()
			time.sleep(3)
			# 点击“确认”按钮
			qrbtn = self.driver.find_element_by_xpath("//div[@class='ui-dialog-buttonset']/button[1]/span[text()='确认']")
			qrbtn.click()
		except Exception as err:
			logger.info("第六步，签约管理-签约管理,合同下载错误信息：")
			logger.error(err)

	# 根据sql查询在数据库中的信息
	def check_sql(self , intoappId):
		sqldb.dbname = "LOAN5DB"
		self.SQL = get_sql("LOANDB", "lb_t_into_info", "intoappId") % intoappId
		cursor = sqldb.executeSQL(self.SQL)
		try:
			self.res = sqldb.get_one(cursor)
			self.auditestate = str(self.res[25])
		except Exception:
			print("SQL查询结果为空！")
			self.logger.exception("SQL查询结果为空！")
		sqldb.closeDB()
		return self.auditestate
	@classmethod
	def tearDownClass(self):
		# 必须使用 @ classmethod装饰器, 所有test运行完后运行一次
		BaseBrowser.quit_browser(self.driver)

if __name__ == '__main__':
	unittest.main()
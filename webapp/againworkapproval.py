# -*- coding:utf-8 -*-
from utils.baseBrowser import BaseBrowser
from webapp.comlogin import test_comLogin
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import time,unittest
from service.myglobal import get_value
from utils.baseLog import MyLog as Log
log = Log.get_log()
logger = log.logger
'''
第五步，信审管理-工作件审批菜单，10035704，万里娜
'''
class test_againWorkapproval(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		# 必须使用@classmethod 装饰器,所有test运行前运行一次
		# 得到driver实例
		self.driver = BaseBrowser.getDriver()
		logger.info("第五步************************againworkapproval.py，信审管理-工作件审批，10035704，万里娜")
	'''
	进入“工作件审批”菜单
	'''
	def test_againworkapp(self):
		try:
			# 根据第一步进件申请，得到“进件编号”
			intoappId = get_value()
			#intoappId = "130154629591"
			logger.info("通过第一步进件申请，得到进件编号：" + intoappId)
			# 进入“信审系统”,与哪个环境
			httpname = "LOANJC5"
			systemname = "credit"
			# 根据用户名，密码，登录方法
			test_comLogin.test_login(self.driver, "10035704", "Cs654321", httpname, systemname)
			# 关闭第一个菜单“工作台”菜单
			self.driver.find_element_by_id("firstMenu0").click()
			time.sleep(3)
			# 打开需要展示的“信审管理”菜单
			self.driver.find_element_by_id("firstMenu3").click()
			# 点“工作件审批”菜单，进入工作件审批页面
			self.driver.find_element_by_xpath("//span[text()=' 工作件审批']").click()
			# 进入“工作件审批”的iframe
			self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@src,'toApprovalWrokFile')]"))
			self.driver.find_element_by_name("intoId").send_keys(intoappId)
			# 点“查询”按钮，查询出该进件编号所有信息
			self.driver.find_element_by_xpath("//span[text()='查询']")
			time.sleep(5)
			# 点“进件编号”链接，进入下一个页面
			self.driver.find_element_by_link_text(intoappId).click()
			# 退出“工作件审批”iframe
			self.driver.switch_to.default_content()
			# 获取当前窗口handle name
			current_window = self.driver.current_window_handle
			time.sleep(3)
			# 获取所有窗口handle name
			all_windows = self.driver.window_handles
			# 切换window，如果window不是当前window，则切换到该window
			for window in all_windows:
				# 新打开的window不等于当前window时
				if window != current_window:
					# 则打开新的window
					self.driver.switch_to.window(window)
			#调用 审核意见标签页方法
			self.auditoption()
		except Exception as err:
			logger.info("再次工作件审批错误信息：")
			logger.error(err)
	'''
	审核意见标签页
	'''
	def auditoption(self):
		try:

			# 点击“审核表”的tab标签页
			self.driver.find_element_by_xpath("//a[text()='审核意见']").click()
			# 进入“审核意见”的iframe
			self.driver.switch_to.frame(
				self.driver.find_element_by_xpath("//iframe[contains(@src,'updateLbTIntoAuditResult')]"))
			# 审批结论
			Select(self.driver.find_element_by_id("dtoauditConclusion")).select_by_value("3100")
			# 通过代码
			Select(self.driver.find_element_by_id("dtoagreeCode")).select_by_value("A101")
			# 审批额度
			self.driver.find_element_by_id("dtoauditAmount").send_keys("35000")
			# 控制拉动滚动条，可见负债率，内部负债率
			# 定位授信依据，定位到元素的源位置
			appr = self.driver.find_element_by_id("dtoinnerReviews")
			# 将鼠标移动到定位的元素上面
			ActionChains(self.driver).move_to_element(appr).perform()
			# 任意点一个文本框，跳出核实收入，回显负债率，内部负债率
			self.driver.find_element_by_id("dtoinnerReviews").click()
			# 点“保存”按钮
			self.driver.find_element_by_xpath("//input[@type='button']").click()
			# 退出“审核意见”的iframe
			self.driver.switch_to.default_content()
			time.sleep(3)
			# 点“提交”按钮
			self.driver.find_element_by_xpath("//input[@value='提交']").click()
			time.sleep(3)
			# 点“确认”按钮
			while 1:
				start = time.clock()
				try:
					self.driver.find_element_by_xpath("//div[@class='ui-dialog-buttonset']/button[1]/span[text()='确认']").click()
					print("已定位到元素!//div[@class='ui-dialog-buttonset']/button[1]/span[text()='确认']")
					logger.info("审核意见通过！！！")
					end = time.clock()
					break
				except Exception as err:
					logger.error(err)
			print('定位耗费时间：' + str(end - start))

		except Exception as err:
			logger.info("审核意见错误信息：")
			logger.error(err)
	@classmethod
	def tearDownClass(self):
		# 必须使用 @ classmethod装饰器, 所有test运行完后运行一次
		BaseBrowser.quit_browser(self.driver)
if __name__=='__main__':
	unittest.main()
	#awapp = test_againWorkapproval()
	#awapp.test_againworkapp()
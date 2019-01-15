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
第四步，信审管理-工作件审批菜单，11043892，王丹
'''
class test_workApproval(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		# 必须使用@classmethod 装饰器,所有test运行前运行一次
		# 得到driver实例
		self.driver = BaseBrowser.getDriver()
		logger.info("第四步************************workapproval.py，信审管理-工作件审批，11043892，王丹")
	'''
	工作件审批方法
	'''
	def test_workapproval(self):
		try:
			# 根据第一步进件申请，得到“进件编号”
			incomId = get_value()
			#incomId = "130154629579"
			logger.info("通过第一步进件申请，得到进件编号：" + incomId)
			# 进入“信审系统”,与哪个环境
			httpname = "LOANJC5"
			systemname = "credit"
			# 用信审专员登录
			test_comLogin.test_login(self.driver, "11043892", "Cs654321", httpname, systemname)
			# 关闭第一个菜单“工作台”菜单
			self.driver.find_element_by_id("firstMenu0").click()
			time.sleep(3)
			# 打开需要展示的“信审管理”菜单
			self.driver.find_element_by_id("firstMenu3").click()
			# 点击“工作件审批”菜单
			self.driver.find_element_by_xpath("//span[text()=' 工作件审批']").click()
			# 进入“工作件审批”iframe
			self.driver.switch_to.frame(
				self.driver.find_element_by_xpath("//iframe[contains(@src,'toApprovalWrokFile')]"))
			time.sleep(5)
			# 获取当前窗口handle name
			current_window = self.driver.current_window_handle
			#输入“进件编号”查询条件
			self.driver.find_element_by_name("intoId").send_keys(incomId)
			# 点击“查询”按钮
			self.driver.find_element_by_xpath("//span[text()='查询']").click()
			# 根据“进件编号”点击，进入下一个页面
			while 1:
				start = time.clock()
				try:
					self.driver.find_element_by_link_text(incomId).click()
					print("已定位到元素！进件编号")
					end = time.clock()
					break
				except:
					print("还未定位到元素！进件编号")
			print('定位耗费时间：' + str(end - start))
			# self.driver.find_element_by_xpath("//td[contains(@id, 'intoAppId')]").click()
			# 退出“工作件审批”iframe
			self.driver.switch_to.default_content()
			time.sleep(3)
			# 获取所有窗口handle name
			all_windows = self.driver.window_handles
			# 切换window，如果window不是当前window，则切换到该window
			for window in all_windows:
				# 新打开的window不等于当前window时
				if window != current_window:
					# 则打开新的window
					self.driver.switch_to.window(window)
			# 调用“调查表”的tab标签
			self.inspectInfo()
			# 调用“信审表”的tab标签
			self.creditInfo()
			# 调用“审核意见”的tab标签
			self.examineview()
		# 操作完成后，返回到当前窗口
		# self.driver.switch_to.window(current_window)
		except Exception as err:
			logger.info("工作件审批错误信息：")
			logger.error(err)
	'''
	打开“调查表”的tab标签页面
	'''
	def inspectInfo(self):
		# 点击“调查表”tab标签页
		self.driver.find_element_by_xpath("//a[text()='调查表']").click()
		time.sleep(3)
		# 进入“调查表”iframe
		self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@src,'toQueryPage')]"))
		# 选中第一条数据，点击“电联”
		self.driver.find_element_by_link_text("电联").click()
		# 退出“调查表”iframe
		self.driver.switch_to.default_content()
		time.sleep(3)
		# 进入“电联调查”iframe
		# self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@src,'toViewInfo')]"))
		# 点击“保存”按钮，保存电联信息
		self.driver.find_element_by_xpath("//span[text()='保存']").click()
		# 点击“关闭”按钮，关闭电联页面
		self.driver.find_element_by_xpath("//span[text()='关闭']").click()
	'''
	打开“信审表”的tab标签页面
	'''
	def creditInfo(self):
		#得到调查表，信审表，审核意见tab页
		# 点击“信审表”的tab标签页
		self.driver.find_element_by_xpath("//a[text()='信审表']").click()
		# 该标签是否已执行
		flag = test_comLogin.isElementExist(self.driver, "icon-ok")
		# 判断未执行时，打开该tab页
		if flag == False:
			time.sleep(3)
			self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@src,'creditAuditView')]"))
			#工作情况，工作方式，选择“雇佣”方式
			Select(self.driver.find_element_by_id("workMode")).select_by_value("01")
			#单位性质
			Select(self.driver.find_element_by_id("companyType")).select_by_value("3")
			#单位所属行业
			Select(self.driver.find_element_by_id("companyIndustry")).select_by_value("Q20")
			#本人在现单位工作年限
			self.driver.find_element_by_id("currentCompanyWorkYear").send_keys("2")
			#家庭情况，婚姻状况
			Select(self.driver.find_element_by_id("maritalStatus")).select_by_value("2")
			#是否有子女
			Select(self.driver.find_element_by_id("childHas")).select_by_value("1")
			#房产信息，名下是否有房
			Select(self.driver.find_element_by_id("houseHas")).select_by_value("0")
			#保存按钮
			self.driver.find_element_by_xpath("//input[@type='button']").click()
			# 退出“信审表”iframe
			self.driver.switch_to.default_content()
		else:
			logger.info("该信审表已执行！！！")
	'''
	审核意见
	'''
	def examineview(self):
		time.sleep(3)
		# 点击“审核表”的tab标签页
		while 1:
			start = time.clock()
			try:
				self.driver.find_element_by_xpath("//a[text()='审核意见']").click()
				print("已定位到元素a[text()='审核意见']")
				end = time.clock()
				break
			except:
				print("还未定位到元素!a[text()='审核意见']")
		print('定位耗费时间：' + str(end - start))
		#进入“审核意见”的iframe
		self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@src,'updateLbTIntoAuditResult')]"))
		#稽查结果，审核-审核结论“同意”
		Select(self.driver.find_element_by_id("dtoauditConclusion")).select_by_value("3100")
		#通过代码
		Select(self.driver.find_element_by_id("dtoagreeCode")).select_by_value("A101")
		#审批金额
		self.driver.find_element_by_id("dtoauditAmount").send_keys("200000")
		#核实收入
		self.driver.find_element_by_id("dtocheckIncome").send_keys("20000")
		# 控制拉动滚动条，可见负债率，内部负债率
		# 定位授信依据，定位到元素的源位置
		appr = self.driver.find_element_by_id("dtoinnerReviews")
		# 将鼠标移动到定位的元素上面
		ActionChains(self.driver).move_to_element(appr).perform()
		#任意点一个文本框，跳出核实收入，回显负债率，内部负债率
		self.driver.find_element_by_id("dtoinnerReviews").click()
		time.sleep(5)
		#点“保存”按钮
		while 1:
			start = time.clock()
			try:
				self.driver.find_element_by_xpath("//*[@id='saveBtn']").click()
				print("已定位到元素!//*[@id='saveBtn']")
				end = time.clock()
				break
			except Exception as err:
				logger.error(err)
				#print("还未定位到元素!input[@type='button'][@value='保存']")
		print('定位耗费时间：' + str(end - start))
		# 退出“审核意见”的iframe
		self.driver.switch_to.default_content()
		# 点击“提交”按钮
		self.driver.find_element_by_xpath("//*[@id='divSubBtnId']/input[2]").click()
		time.sleep(3)
		# 进入“选择下一环节参与者”的iframe
		self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@src,'querySelectPartner')]"))
		# 输入查询条件“用户编号”
		self.driver.find_element_by_name("parUserNo").send_keys("10035704")
		time.sleep(3)
		# 点“查询”按钮，查询出该数据
		self.driver.find_element_by_xpath("//span[text()='查询']").click()
		# 选中第一条数据
		while 1:
			start = time.clock()
			try:
				self.driver.find_element_by_xpath("//input[@type='radio']").click()
				print("已定位到元素!input[@type='radio']")
				end = time.clock()
				break
			except:
				print("还未定位到元素!input[@type='radio']")
		print('定位耗费时间：' + str(end - start))
		# 点“确认”按钮
		self.driver.find_element_by_xpath("//a[text()='确认']").click()
		#退出“选择下一环节参与者”的iframe
		self.driver.switch_to.default_content()
		time.sleep(10)
		#点弹出框“确认”
		self.driver.find_element_by_xpath("/html/body/div[7]/div[3]/div/button[1]/span").click()
	@classmethod
	def tearDownClass(self):
		# 必须使用 @ classmethod装饰器, 所有test运行完后运行一次
		BaseBrowser.quit_browser(self.driver)
if __name__=='__main__':
	unittest.main()
	#wapp = test_workApproval()
	#wapp.test_workapproval()
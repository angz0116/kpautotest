# -*- coding:utf-8 -*-
from selenium import webdriver
import utils.readConfig as readConfig
from utils.baseLog import MyLog as Log
import os, time
log = Log.get_log()
logger = log.logger
"""
获取浏览器的类与方法
"""
class BaseBrowser(object):
	def __init__(self, driver):
		self.driver = driver

	# 判断使用哪个浏览器
	@staticmethod
	def getDriver():
		# 从配置文件中获取浏览器与url地址
		#browser = Config.get_browser("browserName")
		browser = "Chrome"
		logger.info("您选择的浏览器是： %s browser." % browser)
		# 启动浏览器，获取网页源代码
		if browser == "Firefox":
			driver = webdriver.Firefox(executable_path="E:\Program Files (x86)\Mozilla Firefox\\firefox.exe")
			logger.info("Starting firefox browser.")
		elif browser == "Chrome":
			driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\\chromedriver.exe")
			logger.info("Starting Chrome browser.")
		elif browser == "IE":
			driver = webdriver.Ie(executable_path="C:\Program Files (x86)\Internet Explorer\\IEDriverServer.exe")
			logger.info("Starting IE browser.")
		return driver

	@staticmethod
	def open_browser(driver, url):
		#print("========打开浏览器open_brower=========")
		#获取URL地址
		logger.info("获取URL地址是: %s" % url)
		# 获取url地址
		driver.get(url)
		logger.info("打开URL地址: %s" % url)
		driver.maximize_window()
		logger.info("Maximize the current window.")
		#driver.implicitly_wait(10)
		logger.info("Set implicitly wait 10 seconds.")

	#点击退出浏览器driver
	@staticmethod
	def quit_browser(driver):
		logger.info("Now, Close and quit the browser.")
		driver.quit()

	# 浏览器前进操作
	def forward(self):
		self.driver.forward()
		logger.info("Click forward on current page.")

	# 浏览器后退操作
	def back(self):
		self.driver.back()
		logger.info("Click back on current page.")

	# 隐式等待
	def wait(self, seconds):
		self.driver.implicitly_wait(seconds)
		logger.info("wait for %d seconds." % seconds)

	# 点击关闭当前窗口
	def close(self):
		try:
			self.driver.close()
			logger.info("Closing and quit the browser.")
		except NameError as e:
			logger.error("Failed to quit the browser with %s" % e)

	# 回到顶部
	def scroll_top(self):
		js = "var q=document.body.scrollTop=0"
		return self.driver.execute_script(js)

	# 拉到底部
	def scroll_foot(self):
		js = "var q=document.body.scrollTop=10000"
		return self.driver.execute_script(js)
	# 保存图片
	@staticmethod
	def get_window_img(driver,filename):
		#file_path = os.path.dirname(os.path.abspath("."))+"\screenshots\\"+filename+"\\"
		file_path = "D:\\Users\\zhaoai\\PycharmProjects\\leanmationtest\\screenshots\\" + filename + "\\"
		rs = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
		screen_name = file_path + rs +".png"
		try:
			driver.get_screenshot_as_file(screen_name)
		except NameError as e:
			print("保存图片异常信息："+e)

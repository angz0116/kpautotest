# -*- coding:utf-8 -*-
from selenium import webdriver
import  re, time, os
class leantrain():
	def getdriver(self):
		self.driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
		self.driver.maximize_window()
	def pageElement(self):
		driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
		driver.maximize_window()
		driver.get("http://home.baidu.com/contact.html")
		doc = driver.page_source
		emails = re.findall(r'[\w]+@[\w\.-]+', doc)  # 利用正则，找出 xxx@xxx.xxx 的字段，保存到emails列表
		# 循环打印匹配的邮箱
		for email in emails:
			print(email)

	# 保存图片
	def get_window_img(self):
		self.driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
		self.driver.maximize_window()
		print(os.path.abspath("."))
		file_path = os.path.dirname(os.path.abspath("."))+"\screenshots\\"
		self.driver.get("http://home.baidu.com/contact.html")
		rs = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
		screen_name = file_path + rs +".png"
		try:
			self.driver.get_screenshot_as_file(screen_name)
		except NameError as e:
			self.get_window_img()
lr = leantrain()
lr.get_window_img()


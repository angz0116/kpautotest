# -*- coding: utf-8 -*-
from selenium import webdriver
import time,os
from utils import readConfig
#获取html, 得到chrome
def getdriver():
	# 创建chrome参数对象
	option = webdriver.ChromeOptions()
	# 把chrome设置成无界面模式
	option.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
	option.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
	option.add_argument('--no-sandbox') #参数是让Chrome在root权限下跑
	option.add_argument('--window-size=1280,1024')#指定浏览器窗口大小
	option.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
	driver = webdriver.Chrome(executable_path=readConfig.proDir+"/chromedriver.exe", options=option)
	scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
	scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
	driver.set_window_size(scroll_width, scroll_height)
	return driver
#打开html
def openhtml(absPath):
	absurl = "file:///"+absPath
	#返回绝对路径,返回一个文件在当前环境中的绝对路径，这里file 一参数
	url = absurl.replace("\\", "/")
	return url

# 保存截图
def savescreenimg(resultpath):
	driver = getdriver()
	url = openhtml(resultpath)
	driver.get(url)
	time.sleep(3)
	if len(resultpath)>0:
		# 通过切片获取到存储report.html的文件夹
		imgpath = resultpath[:len(resultpath)-11]
		# 把报告截图存放到跟report，log同一目录
		driver.save_screenshot(imgpath + "screenImg.png")
		#pic = ImageGrab.grab()
		#pic.save(imgpath + "screenImg.png")
	driver.quit()

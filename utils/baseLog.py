# -*- coding:utf-8 -*-
import logging
from datetime import datetime
import threading
import os

class Log:
	def __init__(self):
		global logPath, resultPath, proDir
		proDir = os.path.split(os.getcwd())[0]
		resultPath = os.path.join(proDir, "result")
		if not os.path.exists(resultPath):
			os.mkdir(resultPath)
		logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d%H%M%S")))
		if not os.path.exists(logPath):
			os.mkdir(logPath)
		self.logger = logging.getLogger()
		self.logger.setLevel(logging.INFO)
		handler = logging.FileHandler(os.path.join(logPath, "output.log"), encoding="utf-8")
		formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)
		
	def build_start_line(self, case_no):
		self.logger.info("--------" + case_no + " start--------")
	
	def build_end_line(self, case_no):
		self.logger.info("--------" + case_no + " end--------" + "\n\n")
	
	def build_case_line(self, msg, code):
		self.logger.info(str(msg) + ":" + str(code))
	
	def get_report_path(self):
		report_path = os.path.join(logPath, "report.html")
		return report_path
	
	def get_result_path(self):
		return logPath


class MyLog:
	log = None
	mutex = threading.Lock()

	def __init__(self):
		pass

	@staticmethod
	def get_log():
		if MyLog.log is None:
			MyLog.mutex.acquire()
			MyLog.log = Log()
			MyLog.mutex.release()
		return MyLog.log

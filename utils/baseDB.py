# -*- coding:utf-8 -*-
import utils.readConfig as readConfig
from utils.baseLog import MyLog as Log
import pymysql

Config = readConfig.ReadConfig()

class ConfigDB:
	def __init__(self):
		self.dbname = None
		self.log = Log.get_log()
		self.logger = self.log.logger
		self.db = None
		self.cursor = None

	def connectDB(self):
		host = Config.get_db(self.dbname, "host")
		username = Config.get_db(self.dbname, "username")
		password = Config.get_db(self.dbname, "password")
		port = Config.get_db(self.dbname, "port")
		database = Config.get_db(self.dbname, "database")
		#dns = py_mysql.makedsn(str(host), int(port), database)

		try:
			self.db = pymysql.connect(str(host),username, password, database)
			self.cursor = self.db.cursor()
			#print("数据库连接成功")
		except Exception:
			self.logger.error("账号密码错误，数据库登录失败")
		except ConnectionError as ex:
			self.logger.error(str(ex))

	def executeParam(self, sql ,param):
		self.connectDB()
		try:
			self.cursor.execute(sql, param)
			self.db.commit()
		except Exception:
			self.db.rollback()
			self.logger.error("sql为空！")
		return self.cursor

	def executeSQL(self, sql):
		self.connectDB()
		try:
			self.cursor.execute(sql)
			self.db.commit()
		except:
			self.db.rollback()
			self.logger.error("sql为空！")
		return self.cursor
	
	def get_all(self, cursor):
		value = cursor.fetchall()
		return value
	
	def get_one(self, cursor):
		value = cursor.fetchone()
		return value
	
	def closeDB(self):
		self.cursor.close()
		self.db.close()
		#print("数据库关闭!")


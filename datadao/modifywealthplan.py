# -*- coding:utf-8 -*-
from utils.baseDB import ConfigDB
from utils.baseUtils import *
import datetime
sqldb = ConfigDB()
'''
理财计划审批后，根据理财计划编号修改数据库中上线时间，开售时间
'''
class modifyWealthPlan():
	def query_sql(self):
		"""
		self.SQL = get_sql("LCDB", "wms_t_wealth_plan","createtime")
		params = {"starttime":self.endcreatetime, "endtime":self.startcreatetime}
		cursor = sqldb.executeParam(self.SQL, params)
		"""
		sqldb.dbname = "LC1DB"
		self.startcreatetime = datetime.datetime.now().strftime("%Y-%m-%d")
		self.endcreatetime = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
		self.SQL = get_sql("LCDB", "wms_t_wealth_plan", "createtime")%(self.startcreatetime,self.endcreatetime)
		cursor = sqldb.executeSQL(self.SQL)
		try:
			self.res = sqldb.get_all(cursor)
			#查询到理财计划为空，则不进行修改
			if(len(self.res)!=0):
				self.update_sql(self.res)
			else:
				print("未查询到理财计划信息")
		except Exception:
			print("SQL查询结果为空！")
			self.logger.exception("SQL查询结果为空！")
		sqldb.closeDB()
	"""
	根据理财计划编号，修改上线时间，开售时间
	"""
	def update_sql(self , arrList):
		sqldb.dbname = "LC1DB"
		#self.onlineTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		self.onlineTime = "2018-5-10 11:10:00"
		#未查询出修改理财计划数据
		if len(arrList)==0:
			print("根据理财计划编号未查询到需要修改的数据")
		else:#查询出理财计划list，并根据理财计划编号修改上线时间，开售时间
			for arr in arrList:
				self.planNo = arr[1]
				self.SQL = get_sql("LCDB", "wms_t_wealth_plan", "planNo") % (self.onlineTime, self.onlineTime, self.planNo)
				try:
					cursor = sqldb.executeSQL(self.SQL)
					if cursor.rowcount == 1:
						print(self.planNo+"==更新数据成功！")
					else:
						print(self.planNo+"==更新数据失败！")
				except Exception:
					print("SQL查询结果为空！")
					self.logger.exception("SQL查询结果为空！")

if __name__== '__main__':
	modywplan = modifyWealthPlan()
	modywplan.query_sql()
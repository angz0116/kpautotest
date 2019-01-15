# -*- coding:utf-8 -*-

import os
from xlrd import open_workbook
import cx_Oracle
from xlutils.copy import copy
import requests
import json
import random
from datetime import date
import string
from xml.etree import ElementTree as ElementTree


database = {}
proDir = os.path.split(os.getcwd())[0]
dataPath = os.path.join(proDir, "config", "interfaces.xls")
sql_path = os.path.join(proDir, "config", "SQL.xml")

#从SQL.xml中读取SQL数据
def set_xml():
	if len(database) == 0:
		tree = ElementTree.parse(sql_path)
		for db in tree.findall("database"):
			db_name = db.get("name")
			table = {}
			for tb in db.getchildren():
				table_name = tb.get("name")
				sql = {}
				for data in tb.getchildren():
					sql_id = data.get("id")
					sql[sql_id] = data.text.strip()
				table[table_name] = sql
			database[db_name] = table
#从xml文件中获取键值对，数据库及业务表
def get_xml_dict(database_name, table_name):
	set_xml()
	database_dict = database.get(database_name).get(table_name)
	return database_dict
#从xml文件中给where条件字段赋值
def get_sql(database_name, table_name, sql_id):
	db = get_xml_dict(database_name, table_name)
	sql = db.get(sql_id)
	return sql


#从excel中取值
def get_excel(cellname, pid, sheetname):
	cellname = str(cellname)
	pid = str(pid)
	sheetname = str(sheetname)
	fd = open_workbook(dataPath, formatting_info=True)
	sh = fd.sheet_by_name(sheetname)
	for row_index in range(sh.nrows):
		colvalue = sh.cell(int(row_index), 0).value
		if pid == colvalue:
			break
	for col_index in range(sh.ncols):
		rowvalue = sh.cell(0,int(col_index)).value
		if cellname == rowvalue:
			break
	cellvalue = sh.cell(row_index, col_index).value
	return cellvalue
#写入EXCEL
def set_excel(cellvalue, cellname, pid, sheetname):
	cellvalue = str(cellvalue)
	if cellname == "请求报文" or cellname == "返回报文":
		cellvalue = cellvalue.replace(" ", "\n")
	cellname = str(cellname)
	pid = str(pid)
	sheetname = str(sheetname)
	fd = open_workbook(dataPath, formatting_info=True)
	sh = fd.sheet_by_name(sheetname)
	for row_index in range(sh.nrows):
		colValue = sh.cell(int(row_index), 0).value
		if pid == colValue:
			break
	for col_index in range(sh.ncols):
		rowvalue = sh.cell(0, int(col_index)).value
		if cellname == rowvalue:
			break
	sheetIndex = fd._sheet_names.index(sheetname)
	wb = copy(fd)
	sheet = wb.get_sheet(sheetIndex)
	sheet.write(row_index, col_index, cellvalue)
	wb.save(dataPath)
#获取sheet页行数
def get_excelnrows(sheetname):
	sheetname = str(sheetname)
	fd = open_workbook(dataPath, formatting_info=True)
	sh = fd.sheet_by_name(sheetname)
	return sh.nrows

#获取汉字
def get_gbk2312(number):
	str1 = ""
	for i in range(number):
		head = random.randint(0xb0, 0xf7)
		body = random.randint(0xa1, 0xf9)
		val = '{head:x}{body:x}'
		str = bytes.fromhex(val).decode('gb2312')
		str1 += str
	return str1
#根据xls文件名，sheet页名称，打开该sheet页，得到数据
def get_xls(xls_name, sheet_name):
	cls = []
	xlsPath = os.path.join(proDir, "config", xls_name)
	file = open_workbook(xlsPath)
	sheet = file.sheet_by_name(sheet_name)
	nrows = sheet.nrows
	for i in range(1, nrows):
		if True:
			cls.append(sheet.row_values(i))
	return cls

#生成随机数字
def get_number(number):
	s = ''.join(random.choice(string.digits) for i in range(number))
	return s


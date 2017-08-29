import sqlite3
import time
class DBService:
	def __init__(self):
		self.conn = sqlite3.connect('ent.db')
		self.cursor = self.conn.cursor()
		self.creatTable()

	def creatTable(self):
		ent_table="create table if not exists entname(id integer primary key autoincrement,name varchar(20),regNo varchar(30),url varchar(256),time integer)"
		enturls_table="create table if not exists enturl(id integer primary key autoincrement,regNO varchar(30)  not null,urldict text  not null,time integer)"
		self.cursor.execute(ent_table)
		self.cursor.execute(enturls_table)
		self.conn.commit();

	def insert(self,table,params):
		sql1="insert into entname(name,regNo,url,time)values (?,?,?,?) "
		sql2="insert into enturl(regNo,urldict,time) values(?,?,?)"
		if table==1:
			self.cursor.execute(sql1,params)
		else:
			self.cursor.execute(sql2,params)
		self.conn.commit()
		return self.cursor.rowcount

	def query(self,table,params):
		sql1="select url,time from entname where regNo=?"
		sql2="select urldict from enturl where regNo=?"
		if table==1:
			self.cursor.execute(sql1,params)
		else:
			self.cursor.execute(sql2,params)
		return self.cursor.fetchone()

	def delete(self,table,params=()):
		sql1="delete from entname where regNo=?"
		sql2="delete from enturl where regNo=?"
		sql3="delete from entname where time<?"
		sql4="delete from enturl where time<?"
		if table==1:
			self.cursor.execute(sql1,params)
		elif table==2:
			self.cursor.execute(sql2,params)
		else:
			self.cursor.execute(sql3,params)
			self.cursor.execute(sql4,params)
		self.conn.commit()
		return self.cursor.rowcount

	def update(self,params):
		pass

	def __del__(self):
		self.cursor.close()
		self.conn.close()

# if __name__=="__main__":
# 	db = DBService()
# 	# db.insert(1,('a','b','c',int(time.time())))
# 	db.delete(3,(time.time(),))
# 	print(db.query(1,('b',)))
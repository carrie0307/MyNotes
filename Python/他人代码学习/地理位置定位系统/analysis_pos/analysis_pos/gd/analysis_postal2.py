# coding=utf-8
'''
解析whois信息中邮编的地理位置
'''
import sys
from qianduan_format import WebFormat
import MySQLdb
import re

reload(sys)
sys.setdefaultencoding('utf-8')


class Postal2Addr(object):
	def __init__(self):
		self.conn = MySQLdb.connect(host="172.26.253.3", user="root", passwd="platform", db="mal_domain_profile",
									charset='utf8')
		self.cursor = self.conn.cursor()
		self.p_ect0 = [["市", ""], ["省", ""], ["特别行政区", ""], ["维吾尔自治区", ""], ["壮族自治区", ""], ["宁夏回族自治区", ""],
					   ["藏族自治州", ""], ["自治区", ""]]
		self.p_ect1 = [["市", ""], ["地区", ""], ["区", ""], ["县", ""], ["土家族苗族自治州", ""], ["回族自治州", ""], ["蒙古自治州", ""],
				   ["哈萨克自治州", ""], ["柯尔克孜自治州", ""], ["自治州", ""]]

	##type为1表示正常6位解析，2位4位解析，，3为3位解析，，4为解析失败

	def findpos(self,sqls):
		province=None
		city=None
		self.cursor.execute(sqls)
		res = self.cursor.fetchone()
		if (res):
			province = res[0].encode('utf-8')
			city = res[1].encode('utf-8')
			return province,city
		return None


	##输入一个邮编，输出邮编的地理位置和类型,此处的postal一定是去了特殊符号的
	def addr_postal(self,postal):
		global type
		type=0
		global pro_ci
		pro_ci=()
		ll=len(postal)
		if(ll>2):
			if(ll==6):
				sql2="select province,city from location.zip_code1 where code='%s'" % (postal)
				pro_ci=Postal2Addr.findpos(self,sql2)
				if(pro_ci):
					type=1
				else:
					##取4位解析
					sql3='select province,city from location.zip_code1 WHERE code regexp "%s.." LIMIT 1' % (postal[:4])
					pro_ci=Postal2Addr.findpos(self,sql3)
					if pro_ci:
						type = 2
					else:
						##取3位解析
						sql4 = "select province,city from location.zip_code2 WHERE code='%s'" % (postal[:3])
						pro_ci=Postal2Addr.findpos(self,sql4)
						if pro_ci:
							type = 2
						else:
							type=3
							print "解析失败"
			else:
				if(ll>6):
					sql2 = "select province,city from location.zip_code1 where code='%s'" % (postal[:6])
					pro_ci = Postal2Addr.findpos(self, sql2)
					if (pro_ci):
						type = 2
					else:
						##取4位解析
						sql3 = 'select province,city from location.zip_code1 WHERE code regexp "%s.." LIMIT 1' % (postal[:4])
						pro_ci = Postal2Addr.findpos(self, sql3)
						if pro_ci:
							type = 2
						else:
							##取3位解析
							sql4 = "select province,city from location.zip_code2 WHERE code='%s'" % (postal[:3])
							pro_ci = Postal2Addr.findpos(self, sql4)
							if pro_ci:
								type = 2
							else:
								type = 3
								print "解析失败"
				else:
					if(ll>3):
						sql3 = 'select province,city from location.zip_code1 WHERE code regexp "%s.." LIMIT 1' % (postal[:4])
						pro_ci = Postal2Addr.findpos(self, sql3)
						if pro_ci:
							type = 2
						else:
							##取3位解析
							sql4 = "select province,city from location.zip_code2 WHERE code='%s'" % (postal[:3])
							pro_ci = Postal2Addr.findpos(self, sql4)
							if pro_ci:
								type = 2
							else:
								type = 3
								print "解析失败"
					else:
						##取3位解析
						sql4 = "select province,city from location.zip_code2 WHERE code='%s'" % (postal[:3])
						pro_ci = Postal2Addr.findpos(self, sql4)
						if pro_ci:
							type = 2
						else:
							type = 3
							print "解析失败"
		else:
			type=3
			print "解析失败"
		country=None
		if(type==1 or type==2):
			country="中国"
			province=pro_ci[0]
			city=pro_ci[1]
			s = re.compile('特别行政区')
			province = s.sub('', province)
			if city.find('辖')!=-1:
				city=province
			l = WebFormat()
			city = l.change_city(province, city)
			print province
			print  city
			print type
			return country,province,city,type
		else:
			return None,None,None,type

	##主函数
	def get_pos(self,postal):
		print postal
		s=re.compile('\D')
		m=s.match(postal)
		global flag
		flag=0
		if m:
			flag=1
			postal=s.sub('',postal)
		li=Postal2Addr.addr_postal(self,postal)
		type=0
		if li[3]!=3:
			if(flag):
				type=2
			else:type=li[3]
		else:type=3
		print li[0],li[1],li[2],type



	# ##连接数据库
	# def get(self):
	# 	sqlstr = "SELECT domain,postal_code from mal_domain_profile.domain_locate where reg_postal_province is not null and reg_postal_city is null"
	# 	self.cursor.execute(sqlstr)
	# 	result = self.cursor.fetchall()
	# 	cc=0
	# 	for r in result:
	# 		cc=cc+1
	# 		if(r[1]):
	# 			domain=r[0].encode('utf-8')
	# 			postal=r[1].encode('utf-8')
	# 			print domain
	# 			print postal
	# 			s=re.compile('\D')
	# 			m=s.match(postal)
	# 			global flag
	# 			flag=0
	# 			if m:
	# 				flag=1
	# 				postal=s.sub('',postal)
	# 			li=Postal2Addr.addr_postal(self,postal)
	# 			type=0
	# 			if li[3]!=3:
	# 				if(flag):
	# 					type=2
	# 				else:type=li[3]
	# 			else:type=3
	# 			sql5 = "update mal_domain_profile.domain_locate set reg_postal_country=%s,reg_postal_province \
	# 					=%s,reg_postal_city=%s,reg_postal_type=%s where domain=%s"
	# 			data=(li[0],li[1],li[2],type,domain)
	# 			try:
	# 				self.cursor.execute(sql5,data)
	# 				if(cc==1000):
	# 					self.conn.commit()
	# 					cc=0
	# 			except Exception,e:
	# 				print e
	# 				self.conn.rollback()
	# 	self.conn.commit()
	# 	self.conn.close()


if __name__ == '__main__':
	a=Postal2Addr()
	postal='363902'
	a.get_pos(postal)






























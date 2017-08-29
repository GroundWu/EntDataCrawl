#-*-coding:utf-8-*-
import urllib.request
from urllib import parse
import re 
import json
from bs4 import BeautifulSoup
import time
from dbService import DBService
class getInfo:
	def __init__(self):
		self.count=0
	#发送请求
	def get(self,url,postdata={}):
		headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
		postdata=parse.urlencode(postdata).encode('utf-8')
		req=urllib.request.Request(url=url,headers=headers,data=postdata)
		data=''
		try:
			res=urllib.request.urlopen(req,timeout=10)
			data=res.read().decode('utf8')
			print('No.'+str(self.count)+': '+url)
			# print(data)
			self.count+=1
		except:	
			try:
				res=urllib.request.urlopen(req,timeout=15)
				data=res.read().decode('utf8')
				print('Retry==>No.'+str(self.count)+': '+url)
			except:
				data='None'
			# print(data)
		finally:
			if 'invalidLink' in data:
				print('invalidLink...')
			return data

	#连续发送请求,获取分页数据
	def post(self,url):
		data_list=[]
		postdata={}
		totalPage=0
		try:
			jsondata=self.get(url,postdata)
			jsondata=re.sub("<div .*?>.*?</div>|<span .*?>.*?</span>","",jsondata)
			if jsondata!='':
				data=json.loads(jsondata)
				totalPage=data['totalPage']
				perPage=data['perPage']
				data_list.extend(data['data'])
		except:
			print('get post request failed! url:'+url)
		else:
			for page in range(totalPage-1):
				postdata={}
				postdata['draw']=page+1
				postdata['start']=perPage*(page+1)
				postdata['length']=perPage
				try:
					result=self.get(url,postdata)
					result=re.sub("<div .*?>.*?</div>|<span .*?>.*?</span>","",result)
					page_result=json.loads(result)['data']
				except:
					print('get page info failed! url:'+url)
					print(result)
				else:
					data_list.extend(page_result)
					time.sleep(0.1)
		finally:
			return data_list
			
	#获取对应的信息url
	def get_and_store_url(self,regNo):
		host='http://www.gsxt.gov.cn'
		soup=BeautifulSoup(self.html,'html.parser')
		tag=soup.find(class_='mainContent')
		s=tag.script.get_text()
		url_dict=dict(re.findall(r'var\s+(\w+)\s+=\s+\"(.*)\"',s))
		for k,v in url_dict.items():
			url_dict[k]=host+v
		db = DBService()
		jsonstr=json.dumps(url_dict)
		if db.query(2,(regNo,))==None:
			db.insert(2,(regNo,jsonstr,time.time()))
		return url_dict

	#获取基本信息
	def get_basic_info(self,url,regNo):

		self.html=self.get(url)
		self.url_dict=self.get_and_store_url(regNo)

		soup=BeautifulSoup(self.html,"html.parser")
		tag=soup.find(id='primaryInfo')

		result=tag.find_all('dd')
		values=[re.sub('[\s+\：\:\^]','',item.get_text()) for item in result]
		items=tag.find_all('dt')
		keys=[re.sub('[\s+\：\:\^]','',item.get_text()) for item in items]

		primaryInfo=dict(zip(keys,values))
		return primaryInfo

	#获取股东及出资信息
	def get_holders_info(self,url):
		data=self.post(url)
		holders_info=[]
		try:
			# print(data)
			for item in data:
				holder={}
				holder['股东Id']=item['invId']
				holder['股东名称']=item['inv']
				holder['股东类型']=item['invType_CN']
				holder['国籍']=item['country_CN']
				holder['证照类型']=item['blicType_CN']
				holder['证照号码']=item['bLicNo']
				holder['证件类型']=item['cerType_CN']
				holder['证件号码']=item['cerNo']
				holder['详情']=self.get_holder_detail(item['invId'])
				holders_info.append(holder)
		except:
			print("get holders info failed!")
		finally:
			return holders_info

	#获取发起人及出资信息详情		
	def get_holder_detail(self,invId):
		url='http://www.gsxt.gov.cn/corp-query-entprise-info-shareholderDetail-'+invId+'.html'
		data=self.post(url)
		return data

	#获取主要人员信息
	def get_keyperson_info(self,url):
		data=self.post(url)
		keyPersons=[]
		try:			
			for item in data:
				keyperson={}
				keyperson['名称']=item['name']
				keyperson['职位']=item['position_CN']+'(备注：生成的base64编码要删去换行符或回车符)'
				keyPersons.append(keyperson)
		except:
			print('get key person info failed!')
		finally:
			return keyPersons

	#分支管理机构信息
	def get_branchgroup_info(self,url):
		data=self.post(url)
		branchgroups=[]
		try:
			for item in data:
				branchgroup={}
				branchgroup['名称']=item['brName']
				branchgroup['统一社会信用代码/注册号']=item['regNo'].strip()
				branchgroup['登记机关']=item['regOrg_CN']
				branchgroups.append(branchgroup)
		except:
			print('get branchgroup info failed!')
		finally:
			return branchgroups

	#获取变更信息
	def get_alter_info(self,url):
		data=self.post(url)
		alterInfo=[]
		try:
			for item in data:
				alterInfo_item={}
				alterInfo_item['变更事项']=item['altItem_CN']
				alterInfo_item['变更前内容']=item['altBe']
				alterInfo_item['变更后内容']=item['altAf']
				alterInfo_item['变更日期']=item['altDate']
				alterInfo.append(alterInfo_item)
		except:
			print('get alter info failed!')
		finally:
			return alterInfo

	#获取检查结果信息
	def get_spotCheck_info(self,url):
		data=self.post(url)
		spotCheckInfo=[]
		try:
			for item in data:
				spotCheckInfo_item={}
				spotCheckInfo_item['检查实施机关']=item['insAuth_CN']
				spotCheckInfo_item['类型']=item['insType']
				spotCheckInfo_item['日期']=item['insDate']
				spotCheckInfo_item['结果']=item['insRes_CN']
				spotCheckInfo.append(spotCheckInfo_item)
		except:
			print('get spotCheck info failed!')
		finally:
			return spotCheckInfo

	def get_insLicence_info(self,url):
		data=self.post(url)
		try:
			for item in data:
				id=item['licId']
				url_1='http://www.gsxt.gov.cn/corp-query-entprise-info-insLicenceInfoForJs-'+id+'.html'
				res_1=self.get(url_1)
				res_1=json.loads(res_1)
				url_2='http://www.gsxt.gov.cn'+res_1['insLicenceDetailInfoUrl']
				res_2=self.get(url_2)
				detail=json.loads(res_2)
				item['detail']=detail
		except:
			print('get insLicence detail info failed!')
		finally:
			return data

	def get_assist_info(self,url):
		data=self.post(url)
		try:
			for item in data:
				id=item['parent_Id']
				url_1='http://www.gsxt.gov.cn/corp-query-entprise-info-judiciaryStockfreeze-'+id+'.html'
				detail=self.post(url_1)
				item['detail']=detail
		except:
			print('get assistInfo failed!')
		finally:
			return data

	def get_more_info(self,url):
		data=self.post(url)
		# print(data)
		return data

	def get_anCheYear_info(self,url):

		data=self.get(url)
		anCheYearInfo=[]
		try:
			data=json.loads(data)
			for item in data:
				anCheYearInfo_item={}
				anCheYearInfo_item['anCheYear']=item['anCheYear']
				anCheYearInfo_item['anCheId']=item['anCheId']
				anCheYearInfo_item['anCheDate']=item['anCheDate']
				anCheYearInfo_item['anCheYearDetail']=self.get_anCheYear_Detail(item)
				anCheYearInfo.append(anCheYearInfo_item)
		except:
			print('get anCheYear info failed!')
		return anCheYearInfo

	def get_anCheYear_Detail(self,item):
		anCheId=item['anCheId']
		prefix='http://www.gsxt.gov.cn/corp-query-entprise-info-'
		#组装需要请求的url集合
		urls={}
		urls['baseinfo']=prefix+'baseinfo-'+anCheId+'.html'
		urls['webSiteInfo']=prefix+'webSiteInfo-'+anCheId+'.html'
		urls['forInvestment']=prefix+'forInvestment-'+anCheId+'.html'
		urls['sponsor']=prefix+'sponsor-'+anCheId+'.html'
		urls['vAnnualReportAlterstockinfo']=prefix+'vAnnualReportAlterstockinfo-'+anCheId+'.html'
		urls['forGuaranteeinfo']=prefix+'forGuaranteeinfo-'+anCheId+'.html'
		urls['AnnSocsecinfo']=prefix+'AnnSocsecinfo-'+anCheId+'.html'
		urls['annualAlter']=prefix+'annualAlter-'+anCheId+'.html'
		#生成结果字典
		try:
			result={key:self.post(url) for (key,url) in urls.items()}
		except:
			result={}
		finally:
			return result

	# def run(self):
	# 	result={}
	# 	# 基础公示信息
	# 	self.get_basic_info()
	# 	self.get_holders_info(self.url_dict['shareholderUrl'])
	# 	self.get_keyperson_info(self.url_dict['keyPersonUrl'])
	# 	self.get_branchgroup_info(self.url_dict['branchUrl'])
	# 	self.get_more_info(self.url_dict['liquidationUrl'])
	# 	self.get_alter_info(self.url_dict['alterInfoUrl'])
	# 	self.get_more_info(self.url_dict['mortRegInfoUrl'])
	# 	self.get_more_info(self.url_dict['stakQualitInfoUrl'])
	# 	self.get_more_info(self.url_dict['proPledgeRegInfoUrl'])
	# 	self.get_more_info(self.url_dict['trademarkInfoUrl'])
	# 	self.get_spotCheck_info(self.url_dict['spotCheckInfoUrl'])
	# 	self.get_assist_info(self.url_dict['assistUrl'])
		
	# 	#企业提供信息
	# 	##年报
	# 	self.get_anCheYear_info(self.url_dict['anCheYearInfo'])
	# 	self.get_insLicence_info(self.url_dict['insLicenceinfoUrl'])		
	# 	self.url_dict['insInvinfoUrl']
	# 	self.url_dict['insAlterstockinfoUrl'] 
	# 	self.url_dict['insProPledgeRegInfoUrl']
	# 	self.url_dict['insPunishmentinfoUrl']
	# 	self.url_dict['simpleCancelUrl']
	# 	for (k,v) in enterprise_provide_info_url.items():
	# 		enterprise_provide_info[k]=self.get_more_info(v)

		

	# 	#行政许可信息
	# 	self.get_more_info(self.url_dict['otherLicenceDetailInfoUrl'])
	# 	#行政处罚信息
	# 	self.get_more_info(self.url_dict['punishmentDetailInfoUrl'])
	# 	#列入经营异常名录信息
	# 	self.get_more_info(self.url_dict['entBusExcepUrl'])
	# 	#列入严重违法失信企业名单（黑名单）信息
	# 	self.get_more_info(self.url_dict['IllInfoUrl'])


		

	
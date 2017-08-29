from flask import Flask,request,jsonify
from hack import spiderinfo
from getInfo import getInfo
import json
import time
from dbService import DBService
app = Flask(__name__)

prefix = '/entInfo/api/v1.0'
db = DBService()
@app.route(prefix+'/findEnt/<entName>',methods=['GET'])
def findEnt(entName):
	db.delete(3,(time.time()-60,))
	result=spiderinfo(entName)
	return jsonify(result)

@app.route(prefix+'/basicInfo/<id>',methods=['GET'])	
def basicInfo(id):
	# db=DBService()
	url=db.query(1,(id,))[0]
	g=getInfo()
	result=g.get_basic_info(url,id)
	return jsonify(result)
  
@app.route(prefix+'/shareHolderInfo/<id>',methods=['GET'])
def shareHolderInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_holders_info(url_dict['shareholderUrl'])
	return jsonify(result)

@app.route(prefix+'/keyPersonInfo/<id>',methods=['GET'])
def keyPersonInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_keyperson_info(url_dict['keyPersonUrl'])
	return jsonify(result)

@app.route(prefix+'/branchGroupInfo/<id>',methods=['GET'])
def branchGroupInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_branchgroup_info(url_dict['branchUrl'])
	return jsonify(result)

@app.route(prefix+'/liquidationInfo/<id>',methods=['GET'])
def liquidationInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_more_info(url_dict['liquidationUrl'])
	return jsonify(result)

@app.route(prefix+'/alterInfo/<id>',methods=['GET'])
def alterInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_alter_info(url_dict['alterInfoUrl'])
	return jsonify(result)

@app.route(prefix+'/mortRegInfo/<id>',methods=['GET'])
def mortRegInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_more_info(url_dict['mortRegInfoUrl'])
	return jsonify(result)

@app.route(prefix+'/stakQualitInfo/<id>',methods=['GET'])
def stakQualitInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_more_info(url_dict['stakQualitInfoUrl'])
	return jsonify(result)

@app.route(prefix+'/proPledgeRegInfo/<id>',methods=['GET'])
def proPledgeRegInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_more_info(url_dict['proPledgeRegInfoUrl'])
	return jsonify(result)

@app.route(prefix+'/trademarkInfo/<id>',methods=['GET'])
def trademarkInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_more_info(url_dict['trademarkInfoUrl'])
	return jsonify(result)

@app.route(prefix+'/spotCheckInfo/<id>',methods=['GET'])
def spotCheckInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_spotCheck_info(url_dict['spotCheckInfoUrl'])
	return jsonify(result)

@app.route(prefix+'/assistInfo/<id>',methods=['GET'])
def assistInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_assist_info(url_dict['assistUrl'])
	return jsonify(result)

@app.route(prefix+'/insLicenInfo/<id>',methods=['GET'])
def insLicenInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_insLicence_info(url_dict['insLicenceinfoUrl'])
	return jsonify(result)

@app.route(prefix+'/insInvInfo/<id>',methods=['GET'])
def insInvInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_more_info(url_dict['insInvinfoUrl'])
	return jsonify(result)

@app.route(prefix+'/insAlterstockInfo/<id>',methods=['GET'])
def insAlterstockInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_more_info(url_dict['insAlterstockinfoUrl'])
	return jsonify(result)

@app.route(prefix+'/insProPledgeRegInfo/<id>',methods=['GET'])
def insProPledgeRegInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_more_info(url_dict['insProPledgeRegInfoUrl'])
	return jsonify(result)

@app.route(prefix+'/insPunishmentInfo/<id>',methods=['GET'])
def insPunishmentInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_more_info(url_dict['insPunishmentinfoUrl'])
	return jsonify(result)

@app.route(prefix+'/simpleCancelInfo/<id>',methods=['GET'])
def simpleCancelInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_more_info(url_dict['simpleCancelUrl'])
	return jsonify(result)


@app.route(prefix+'/otherLicenceDetailInfo/<id>',methods=['GET'])
def otherLicenceDetailInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_more_info(url_dict['otherLicenceDetailInfoUrl'])
	return jsonify(result)

@app.route(prefix+'/punishmentDetailInfo/<id>',methods=['GET'])
def punishmentDetailInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_more_info(url_dict['punishmentDetailInfoUrl'])
	return jsonify(result)

@app.route(prefix+'/entBusExcep/<id>',methods=['GET'])
def entBusExcep(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_more_info(url_dict['entBusExcepUrl'])
	return jsonify(result)

@app.route(prefix+'/illInfo/<id>',methods=['GET'])
def illInfo(id):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_more_info(url_dict['IllInfoUrl'])
	return jsonify(result)
@app.route(prefix+'/anCheYearInfo/<id>/<year>',methods=['GET'])
def anCheYearInfo(id,year):
	# db=DBService()
	url_json=db.query(2,(id,))[0]
	url_dict=json.loads(url_json)
	g=getInfo()
	result=g.get_anCheYear_info(url_dict['anCheYearInfo'])
	return jsonify(result)

if __name__=="__main__":
	app.run();

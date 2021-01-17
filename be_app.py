from flask import Flask, escape, request,jsonify
from db import DbHandler,IndexedMeasure

dbh=DbHandler()

app = Flask(__name__)

@app.route('/be/patient/<p_id>',methods=['POST'])
def add_patient(p_id):
    #Add patient to database
    #p_id coresponds to number in http://tesla.iem.pw.edu.pl:9080/v2/monitor
    #in body of request should be json like one posted on monitor ^
     success,resp=dbh.init_patient(IndexedMeasure(request.json,p_id))
     return resp, 200 if(success) else 422



@app.route('/be/measure/<p_id>',methods=['POST'])
def post_measure(p_id):
    # Insers measure json to db
    #in body of request should be json like one posted on monitor ^
     print(request.json)
     success,resp=dbh.insert_measure(IndexedMeasure(request.json,p_id))
     return resp, 200 if(success) else 422


@app.route('/be/measure/<p_id>/<from_ts>/<to_ts>/',methods=['GET'])
def get_measure(p_id=None,from_ts="",to_ts=""):

     # Posts list of measures from p_id patient, between timestamps
     # for default args takes for all values 
     # ts should be formatted like:
     # 2021-01-11+20:18:43
     # returns list of monitor's jasons + field "ts" for recording timestamps

     r=dbh.get_measures(p_id,from_ts.replace('+',' '),to_ts.replace('+',' '))
     return jsonify(r),200


@app.route('/be/measure/<p_id>/',methods=['GET'])
def get_measure1(p_id):
     r=dbh.get_measures(p_id,"","")
     return jsonify(r),200

@app.route('/be/measure/',methods=['GET'])
def get_measure2():
     r=dbh.get_measures(None,"","")
     return jsonify(r),200



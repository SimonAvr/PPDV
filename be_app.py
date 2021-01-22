from flask import Flask, escape, request,jsonify, json
from db import DbHandler,IndexedMeasure
from recorder import fetch_data()

dbh=DbHandler()

app = Flask(__name__)
playback=[]
realtime=False
playback_it=0
@app.route('/be/playback',methods=['GET'])
def get_playback():
        global playback_it
        global playback
        if not realtime and len(playback)>0:
            if playback_it>=len(playback):
                    playback_it=0
            else:
                    playback_it+=1
            return  playback[playback_it]
        else:
            return dict()

@app.route('/be/playback/<p_id>',methods=['GET'])
def get_playback_id(p_id):
    return fetch_data(p_id)


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
#    print(request.json)
     success,resp=dbh.insert_measure(IndexedMeasure(request.json,p_id))
#    print(resp)
     return resp, 200 if(success) else 422


@app.route('/be/measure/<p_id>/<from_ts>/<to_ts>/',methods=['GET'])
def get_measure(p_id=None,from_ts="",to_ts=""):

     # Posts list of measures from p_id patient, between timestamps
     # for default args takes for all values 
     # ts should be formatted like:
     # 2021-01-11+20:18:43
     # returns list of monitor's jasons + field "ts" for recording timestamps

     r=dbh.get_measures(p_id,from_ts.replace('+',' '),to_ts.replace('+',' '))
     global playback
     playback=r
     return jsonify(r),200


@app.route('/be/measure/<p_id>/',methods=['GET'])
def get_measure1(p_id):
     r=dbh.get_measures(p_id,"","")
     global playback
     playback=r
     return jsonify(r) ,200

@app.route('/be/measure/',methods=['GET'])
def get_measure2():
     r=dbh.get_measures(None,"","")
     global playback
     playback=r
     return jsonify(r),200



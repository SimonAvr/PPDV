import requests
import mysql.connector
import json
import datetime
class IndexedMeasure:
    def __init__(self,d,url_id):
        self.d=d
        self.url_id=url_id
    def str_entry(self):
        return json.dumps(self.d)
def get_str_result(cursor):
    ret=""
    for r in cursor.fetchall():
        ret+=str(r)
    return ret


#def insert_mesure(i):
#    s=fetch_data(i)["trace"]["sensors"]
#    d=dict()
#    for ss in s:
#        for s3 in ss:
#            print(s3)

class DbHandler:
    def __init__(self):
       self.connect()

          # for s3 in ss:
          #     print(s3)

    def connect(self):
        self.db=mysql.connector.connect(
          host="localhost",
          user="user",
          password="1234"
        )
        self.cursor=self.db.cursor()
    def close(self):
        self.cursor.close()
        self.db.close()


    def init_patient(self,indexed_measure ):
        lastname=indexed_measure.d["lastname"]
        firstname=indexed_measure.d["firstname"]
        disabled=indexed_measure.d["disabled"]
        url_id=indexed_measure.url_id
        self.cursor.execute("use stepdb;" )
        q=f"insert into patient (url_id, firstname,lastname,disabled) \
                values( {url_id}, '{firstname}', '{lastname}', {disabled} );"
        print(q)
        self.cursor.execute(q)
        result=cursor.fetchall()
        ret=False
        try:
            self.db.commit()
            ret= True
        except MySQLdb.IntegrityError:
            ret=False
        return ret,result


    def insert_measure(self,indexed_measure ):
        self.connect()
        q=(f"insert into measure (patient_id,entry)\
                values( \
                {indexed_measure.url_id}, \
                \'{indexed_measure.str_entry()}\' \
                );")
     #  print('\n')
     #  print(q)
     #  print('\n')
        self.cursor.execute("use stepdb;" )
        self.cursor.execute(q)
        try:
            self.db.commit()
            ret= True
        except MySQLdb.IntegrityError:
            print("IntegrityError")
            ret=False
#       finally:
#           print(f"finally { result}"
#       print(f"End result {result}")
        self.cursor.close()
        self.db.close()
        return ret,""



    def get_measures(self,patient_id,from_time,to_time):
        self.connect()
        self.cursor.execute("use stepdb;")
        q=f"select entry, ts from measure \
                where \
                { '' if from_time == '' else f' ts < {from_time} and '   }\
                { '' if to_time == '' else f' ts > {to_time} and '   }\
                { '1=1' if patient_id is None else f'patient_id={patient_id}'}"
        print(q)
        self.cursor.execute(q)
        r=self.cursor.fetchall()
#       print(r)
        ret=[]
        for rr in r:
            jj,ts=rr
           #jj=jj.replace('false','False')
           #jj=jj.replace(' ','')
           #jj=jj.replace('\t','')
            jj=jj[1:-1]
            print('\n')
            print(jj)
            print('\n')
            d=json.loads(jj)
            ret.append(d)
        self.close()
        return ret


#init_patient(im,mycursor)

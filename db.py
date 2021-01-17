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


def print_cursor(cursor):
    result=cursor.fetchall()
    for x in result:
        print(x)


def insert_mesure(i):
    s=fetch_data(i)["trace"]["sensors"]
    d=dict()
    for ss in s:
        for s3 in ss:
            print(s3)

class DbHandler:
    def __init__(self):
        self.db=mysql.connector.connect(
          host="localhost",
          user="user",
          password="1234"
        )
        self.cursor=self.db.cursor()

          # for s3 in ss:
          #     print(s3)


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
        finally:
            self.cursor.close()
            return ret,result


    def insert_measure(self,indexed_measure ):
        q=(f"insert into measure (patient_id,entry)\
                values( \
                {indexed_measure.url_id}, \
                \'{indexed_measure.str_entry()}\' \
                );")
        print('\n')
        print(q)
        print('\n')
        self.cursor.execute("use stepdb;" )
        result=self.cursor.execute(q)
        try:
            self.db.commit()
            ret= True
        except MySQLdb.IntegrityError:
            ret=False
        finally:
            self.cursor.close()
            return ret,result



    def get_measures(self,patient_id,from_time,to_time):
        self.cursor.execute("use stepdb;")
        q=f"select entry, ts from measure \
                where \
                { '' if from_time == '' else f' ts < {from_time} and '   }\
                { '' if to_time == '' else f' ts > {to_time} and '   }\
                { '1=1' if patient_id is None else f'patient_id={patient_id}'}"
        print(q)
        self.cursor.execute(q)
        r=self.cursor.fetchall()
        ret=[]
        for rr in r:
            jj,ts=rr
            d=json.loads(jj)
            d['ts']=ts
            ret.append(d)
        self.cursor.close()
        return ret


#init_patient(im,mycursor)

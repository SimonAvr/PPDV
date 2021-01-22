import requests
import json
import time
def fetch_data(i):
   r=requests.get(f"http://tesla.iem.pw.edu.pl:9080/v2/monitor/{i}")
   return r.json()
#   return '{ "disabled": false,\
# "firstname": "Janek",\
# "id": 12,\
# "lastname": "Grzegorczyk",\
# "trace": {\
#   "id": 2581201012010,\
#   "name": "bach",\
#   "sensors": [\
#     {\
#       "anomaly": false,\
#       "id": 0,\
#       "name": "L0",\
#       "value": 738\
#     },\
#     {\
#       "anomaly": false,\
#       "id": 1,\
#       "name": "L1",\
#       "value": 673\
#     },\
#     {\
#       "anomaly": false,\
#       "id": 2,\
#       "name": "L2",\
#       "value": 1023\
#     },\
#     {\
#       "anomaly": false,\
#       "id": 3,\
#       "name": "R0",\
#       "value": 1023\
#     },\
#     {\
#       "anomaly": false,\
#       "id": 4,\
#       "name": "R1",\
#       "value": 168\
#     },\
#     {\
#       "anomaly": false,\
#       "id": 5,\
#       "name": "R2",\
#       "value": 1023\
#     }\
#   ]\
# }\
#\
#
def record():
    while True:
        for i in range(1,2):
            r=fetch_data(i)
#            print(r)
            requests.post(f'http://127.0.0.1:5000/be/measure/{i}',json=r)
            time.sleep(0.1)
#TODO make it on separate thread and run/start by socket/ webapi?
if __name__=="__main__":
    record()

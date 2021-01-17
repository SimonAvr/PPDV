import requests
import json
import time
def fetch_data(i):
    r=requests.get(f"http://tesla.iem.pw.edu.pl:9080/v2/monitor/{i}")
    return r.json()
def record():
    while True:
        for i in range(1,2):
            r=fetch_data(i)
#            print(r)
            requests.post(f'http://127.0.0.1:5000/be/measure/{i}',json=r)
            time.sleep(0.1)
#TODO make it on separate thread and run/start by socket/ webapi?
record()

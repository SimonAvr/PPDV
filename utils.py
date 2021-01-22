import urllib, json
import requests


url1 = 'http://tesla.iem.pw.edu.pl:9080/v2/monitor/1'

def getTrace(data):
    res = []
    trace =  (data['trace']['sensors'])
    for t in trace:
        res.append(t['value'])    
    return res

def deser_measure(s):
    for l in s:
        print(s)

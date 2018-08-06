# -*- coding: utf-8 -*-
import os
import sys
import io
import re
import json

basedir = os.path.abspath(os.path.dirname(__file__))

fpth = os.path.join(basedir,'bigmeter.json')
fo = os.path.join(basedir,'bigsdafe.json')
fmeter = os.path.join(basedir,'meter_shexian.json')
fstation = os.path.join(basedir,'staion_shexian.json')

fi = io.open(fpth,encoding='utf-8')
fo = open(fo,'w')
fmetero = open(fmeter,'w')
fstationo = open(fstation,'w')

def station(i,name,ust,lng,lat,coortype):
    statn = {
      "model": "dmam.station",
      "pk": i,
      "fields": {
        "username": name,
        "description": "",
        "usertype": ust,
        "madedate": "2018-08-02",
        "lng": lng,
        "lat": lat,
        "coortype": coortype,
        "locate": "None",
        "belongto": 1,
        "meter": i
      }
    }
    return statn

def meter(i,serialnumber,dn):
    met = {
      "model": "dmam.meter",
      "pk": i,
      "fields": {
        "serialnumber": serialnumber,
        "simid": i,
        "version": "200",
        "dn": dn,
        "metertype": "\u6c34\u8868",
        "belongto": 1,
        "mtype": "0",
        "protocol": "0",
        "R": "100",
        "q3": "100",
        "check_cycle": "10",
        "state": "1"
      }
    }
    
    return met

def simcard(i,data):
    sim = {
      "model": "dmam.simcard",
      "pk": i,
      "fields": {
        "simcardNumber": data,
        "belongto": 3,
        "isStart": "1",
        "operator": "\u4e2d\u56fd\u79fb\u52a8",
        "create_date": "2018-08-02T16:07:57.299",
        "update_date": "2018-08-02T16:07:57.400",
      }
    }
    return sim

def jsonop():
    jsonstr = json.load(fi)
    print(len(jsonstr))
    print(jsonstr[0],type(jsonstr[0]))
    sim_list = []
    meter_list =[]
    station_list = []
    i=1
    for s in jsonstr:
        simno=s["fields"]["simid"]
        sim_list.append(simcard(i,simno))
        serialnumber=s["fields"]["serialnumber"]
        dn=s["fields"]["dn"]
        meter_list.append(meter(i,serialnumber,dn))
        
        username=s["fields"]["username"]
        usertype=s["fields"]["usertype"]
        lng=s["fields"]["lng"]
        lat=s["fields"]["lat"]
        coortype=s["fields"]["coortype"]
        
        station_list.append(station(i,username,usertype,lng,lat,coortype))
        
        i+=1
        
    fo.write(json.dumps(sim_list,indent=2))
    fmetero.write(json.dumps(meter_list,indent=2))
    fstationo.write(json.dumps(station_list,indent=2))

jsonop()

def couri():
    flag = 0
    for line in fi:
        if '发送'.decode('utf-8') in line:
            flag = 1
            continue
        if flag:
            flag = 0
            continue
        if '接收'.decode('utf-8') in line:
            continue
        fo.write(line)
        
    fo.close()
    fi.close()

# couri()

    
def grad4():
    for line in f:
        #print line
        cis=[]
        pis=[]
        for idx,words in enumerate(line.split()):
            if idx ==0:
                #word0= words.split(u'、')
                word0= words.split(u'.')
                num = word0[0]
                w = word0[1]
                #m=re.split('[(,)]',w)
                ci = w[0]
                if w[1] == '(':
                    pi = w[2:-1]
                else:
                    pi = w[1:]
            else:
                ci = words[0]
                if words[1] == '(':
                    pi = words[2:-1]
                else:
                    pi = words[1:]
            
            cis.append(ci)
            pis.append(pi)
        print num,' '.join(pis)
        print '\t'+' '.join(cis)
                
                
        
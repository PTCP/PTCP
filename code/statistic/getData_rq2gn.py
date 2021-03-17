import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
import copy
import matplotlib.pyplot as plt
import sys

def tree(): return defaultdict(tree)

def readFile(pathfile):
    f = open(pathfile)
    content = f.read()
    f.close()
    return content.splitlines()

if __name__ == "__main__":
    path = '../../subjects/'
    subjects = readFile(path + 'uselist-gnadd-all')
    apps = ['greedytotal_withouttime.txt','greedyadditional_withouttime.txt','genetic_withouttime.txt','arp_withouttime.txt','greedytotal_withtime.txt','greedyadditional_withtime.txt','genetic_withtime.txt','arp_withtime.txt','random']
    apfdc = []
    ft = []
    at = []
    for app in apps:
        apfdc.append([])
        ft.append([])
        at.append([])
    gn = [50,100,200]
    ts = [1.5]
    tosem_path = 'testmethod/dynamic'
    gran = 'state'
    result = tree()
    for subject in subjects:
        spath = path + subject + '/' + tosem_path + '/'
        for gitem in gn:
            for titem in ts:
                tb = [0]*len(apps)
                tmax = 0
                for i in range(len(apps)):
                    app = apps[i]
                    if app !='random':
                        temp = eval(readFile(spath + gran + '/' + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/apfdc_total/' + app)[0])
                        apfdc[i].append(temp)
                        tb[i] = temp
                        tmax = max(temp,tmax)
                        tempf = eval(readFile(spath + gran + '/' + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/dectedtime/firsttime/' + app)[0])
                        tempa = eval(readFile(spath + gran + '/' + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/dectedtime/averagetime/' + app)[0])
                        ft[i].append(tempf)
                        at[i].append(tempa)
                        result[subject][gitem][titem][app]['ft'] = tempf
                        result[subject][gitem][titem][app]['at'] = tempa
                        result[subject][gitem][titem][app]['apfdc'] = temp
                    else:
                        rt = []
                        for j in range(50):
                            temp = eval(readFile(spath + gran + '/' + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/apfdc_total/' + app + str(j) + '.txt')[0])
                            rt.append(temp)
                        tb[i] = sum(rt)/(len(rt)*1.0)
                        apfdc[i].append(sum(rt)/(len(rt)*1.0))
                        tmax = max(tmax,sum(rt)/(len(rt)*1.0))
                        tempf = eval(readFile(spath + gran + '/' + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/dectedtime/firsttime/' + app)[0]) 
                        tempa = eval(readFile(spath + gran + '/' + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/dectedtime/averagetime/' + app)[0])
                        ft[i].append(tempf)
                        at[i].append(tempa)
                        result[subject][gitem][titem][app]['ft'] = tempf
                        result[subject][gitem][titem][app]['at'] = tempa
                        result[subject][gitem][titem][app]['apfdc'] = sum(rt)/(len(rt)*1.0)

    app_list = ['UGT','UGA','UGE','UARP','AGT','AGA','AGE','AARP','RANDOM']
    data = {}
    for i in range(len(app_list)):
        data[app_list[i]] = copy.deepcopy(apfdc[i])
    df = pd.DataFrame(data)

    metrics = ['apfdc','ft','at'] 
    for metric in metrics:
        f = open('data_gn/%s_all.csv'%metric,'w')
        for app in app_list:
            f.write('%s,'%app)
        f.write('subject,gn,ts\n')
        for subject in subjects:
            for gitem in gn:
                for titem in ts:
                    for i in range(len(apps)):
                        f.write('%s,'%result[subject][gitem][titem][apps[i]][metric])
                    f.write('%s,%s,%s\n'%(subject,gitem,titem))
        f.close()

    for metric in metrics:
        for gitem in gn:
            f = open('data_gn/%s_all_%s.csv'%(metric,gitem),'w')
            for app in app_list:
                f.write('%s,'%app)
            f.write('subject,gn,ts\n')
            for subject in subjects:
                for titem in ts:
                    for i in range(len(apps)):
                        f.write('%s,'%result[subject][gitem][titem][apps[i]][metric])
                    f.write('%s,%s,%s\n'%(subject,gitem,titem))
            f.close()

    for metric in metrics:
        for titem in ts:
            f = open('data_gn/%s_all_%s.csv'%(metric,titem),'w')
            for app in app_list:
                f.write('%s,'%app)
            f.write('subject,gn,ts\n')
            for subject in subjects:
                for gitem in gn:
                    for i in range(len(apps)):
                        f.write('%s,'%result[subject][gitem][titem][apps[i]][metric])
                    f.write('%s,%s,%s\n'%(subject,gitem,titem))
        f.close()



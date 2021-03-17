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
    subjects = readFile(path + 'uselist-all')
    apps = ['greedytotal_withouttime.txt','greedyadditional_withouttime.txt','genetic_withouttime.txt','arp_withouttime.txt','greedytotal_withtime.txt','greedyadditional_withtime.txt','genetic_withtime.txt','arp_withtime.txt','random']
    apfdc = []
    ft = []
    at = []
    best = [0] * len(apps)
    baseline = [0] * len(apps)
    baselineeq = [0] * len(apps)
    for app in apps:
        apfdc.append([])
        ft.append([])
        at.append([])
    gn = [4,8,12,16]
    ts = [1.25,1.5,1.75,2.0]
    result = tree()
    for subject in subjects:
        spath = path + subject + '/testmethod/dynamic/state/'
        for gitem in gn:
            for titem in ts:
                tb = [0]*len(apps)
                tmax = 0
                for i in range(len(apps)):
                    app = apps[i]
                    if app !='random':
                        temp = eval(readFile(spath + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/apfdc_total/' + app)[0])
                        apfdc[i].append(temp)
                        tb[i] = temp
                        tmax = max(temp,tmax)
                        tempf = eval(readFile(spath + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/dectedtime/firsttime/' + app)[0])
                        tempa = eval(readFile(spath + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/dectedtime/averagetime/' + app)[0])
                        ft[i].append(tempf)
                        at[i].append(tempa)
                        result[subject][gitem][titem][app]['ft'] = tempf
                        result[subject][gitem][titem][app]['at'] = tempa
                        result[subject][gitem][titem][app]['apfdc'] = temp
                    else:
                        rt = []
                        for j in range(50):
                            temp = eval(readFile(spath + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/apfdc_total/' + app + str(j) + '.txt')[0])
                            #apfdc[i].append(temp)
                            rt.append(temp)
                        tb[i] = sum(rt)/(len(rt)*1.0)
                        apfdc[i].append(sum(rt)/(len(rt)*1.0))
                        tmax = max(tmax,sum(rt)/(len(rt)*1.0))
                        tempf = eval(readFile(spath + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/dectedtime/firsttime/' + app)[0]) 
                        tempa = eval(readFile(spath + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/dectedtime/averagetime/' + app)[0])
                        ft[i].append(tempf)
                        at[i].append(tempa)
                        result[subject][gitem][titem][app]['ft'] = tempf
                        result[subject][gitem][titem][app]['at'] = tempa
                        result[subject][gitem][titem][app]['apfdc'] = sum(rt)/(len(rt)*1.0)
                for i in range(len(apps)):
                    if apfdc[i][-1] > apfdc[-1][-1]:
                        baseline[i] += 1
                    elif apfdc[i][-1] == apfdc[-1][-1]:
                        baselineeq[i] += 1
                    else:
                        #baseline[-1] += 1
                        pass
                for i in range(len(apps)):
                    if tb[i] == tmax:
                        best[i] += 1

    for i in range(len(apfdc)):
        print(str(apps[i]) + ' : ' + ("%.4f" % (sum(apfdc[i])/(len(apfdc[i])*1.0))) + '  -   ' + str(best[i]) + '/' + str(len(apfdc[i])))
    print(baseline)
    print(baselineeq)
    app_list = ['UGT','UGA','UGE','UARP','AGT','AGA','AGE','AARP','RANDOM']
    data = {}
    for i in range(len(app_list)):
        data[app_list[i]] = copy.deepcopy(apfdc[i])
    df = pd.DataFrame(data)
    print(df)
    df.to_csv('data_overall/boxplotview_all.csv')
    f = open('data_overall/boxplot_time_test.csv','w')
    f.write('order,apfdc,ft,at,techniques' + '\n')
    
    for i in range(len(app_list)):
        for j in range(len(apfdc[i])):
            f.write(str(i) + ',' + str(apfdc[i][j]) + ',' + str(ft[i][j]/(1*1.0)) + ',' + str(at[i][j]/(1*1.0)) + ',' + str(app_list[i]) + '\n')
    f.close()

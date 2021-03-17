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
    apps = ['greedytotal_withouttime.txt','greedyadditional_withouttime.txt','genetic_withouttime.txt','arp_withouttime.txt','greedytotal_withtime.txt','greedyadditional_withtime.txt','genetic_withtime.txt','arp_withtime.txt','GroupTTMethod','GroupGAMethod','GroupGeneticMethod','GroupARTMethod','SAGT','GroupTAMethod','SAARP','random']
    apfdc = []
    ft = []
    at = []
    for app in apps:
        apfdc.append([])
        ft.append([])
        at.append([])
    gn = [4,8,12,16]
    ts = [2.0]
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
                    subject_path_n = spath + gran + '/'
                    g = gitem
                    tc = titem
                    if app == 'SAGT':
                       	temp_apfdc = eval(readFile(subject_path_n + str(20.0) + 'avg-new/evaluate/' + str(g) + '/apfdc_total/' + 'greedytotal_withtime.txt')[0])
                    	temp_ft = eval(readFile(subject_path_n + str(20.0) + 'avg-new/evaluate/' + str(g) + '/dectedtime/firsttime/' + 'greedytotal_withtime.txt')[0])
                    	temp_at = eval(readFile(subject_path_n + str(20.0) + 'avg-new/evaluate/' + str(g) + '/dectedtime/averagetime/' + 'greedytotal_withtime.txt')[0])
                        apfdc[i].append(temp_apfdc)
                        tb[i] = temp_apfdc
                        tmax = max(temp_apfdc,tmax)
                    	result[subject][g][tc]['SAGT']['apfdc'] = temp_apfdc
                    	result[subject][g][tc]['SAGT']['ft'] = temp_ft
                    	result[subject][g][tc]['SAGT']['at'] = temp_at 
                    elif app == 'SAARP':
			temp_apfdc = eval(readFile(subject_path_n + str(20.0) + 'avg-new/evaluate/' + str(g) + '/apfdc_total/' + 'arp_withtime.txt')[0])
                    	temp_ft = eval(readFile(subject_path_n + str(20.0) + 'avg-new/evaluate/' + str(g) + '/dectedtime/firsttime/' + 'arp_withtime.txt')[0])
                    	temp_at = eval(readFile(subject_path_n + str(20.0) + 'avg-new/evaluate/' + str(g) + '/dectedtime/averagetime/' + 'arp_withtime.txt')[0])
                        apfdc[i].append(temp_apfdc)
                        tb[i] = temp_apfdc
                        tmax = max(temp_apfdc,tmax)
                    	result[subject][g][tc]['SAARP']['apfdc'] = temp_apfdc
                    	result[subject][g][tc]['SAARP']['ft'] = temp_ft
                    	result[subject][g][tc]['SAARP']['at'] = temp_at
                    elif app !='random':
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
                            #apfdc[i].append(temp)
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

    app_list = ['UGT','UGA','UGE','UARP','AGT','AGA','AGE','AARP','SUGT','SUGA','SUGE','SUARP','SAGT','SAGA','SAARP','RANDOM']
    #app_list = ['UGT','UGA','UARP','AGT','AGA','AARP','RANDOM']
    data = {}
    for i in range(len(app_list)):
        data[app_list[i]] = copy.deepcopy(apfdc[i])
    df = pd.DataFrame(data)

    metrics = ['apfdc','ft','at'] 
    for metric in metrics:
        f = open('data_seq/%s_all.csv'%metric,'w')
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
            f = open('data_seq/%s_all_%s.csv'%(metric,gitem),'w')
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
            f = open('data_seq/%s_all_%s.csv'%(metric,titem),'w')
            for app in app_list:
                f.write('%s,'%app)
            f.write('subject,gn,ts\n')
            for subject in subjects:
                for gitem in gn:
                    for i in range(len(apps)):
                        f.write('%s,'%result[subject][gitem][titem][apps[i]][metric])
                    f.write('%s,%s,%s\n'%(subject,gitem,titem))
        f.close()



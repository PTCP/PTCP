import os
import numpy
import copy
from collections import defaultdict
import sys

def tree(): return defaultdict(tree)

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()


if __name__ == '__main__':
    path = '../../subjects/'
    subjects = readFile(path + 'uselist-all')
    subjectsdict = {}
    for i in range(len(subjects)):
        subjectsdict[subjects[i].lower()] = subjects[i]
    indexlist = copy.deepcopy(subjectsdict.keys())
    indexlist.sort()
    apps = ['greedytotal_withouttime.txt','greedyadditional_withouttime.txt','genetic_withouttime_dict.txt','arp_withouttime.txt','greedytotal_withtime.txt','greedyadditional_withtime.txt','genetic_withtime.txt','arp_withtime.txt','random']
    gn = [4,8,12,16]
    ts = [1.25,1.5,1.75,2.0]
    result = defaultdict(tree)
    rtime = defaultdict(tree)
    for flag in indexlist:
        subject = subjectsdict[flag]
        spath = path + subject + '/testmethod/dynamic/state/'
        apfdc = []
        best = [0] * len(apps)
        for app in apps:
            apfdc.append([])
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
                        result[flag][gitem][titem][app] = temp
                    else:
                        rt = []
                        for j in range(50):
                            temp = eval(readFile(spath + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/apfdc_total/' + app + str(j) + '.txt')[0])
                            rt.append(temp)
                        tb[i] = sum(rt)/(len(rt)*1.0)
                        apfdc[i].append(sum(rt)/(len(rt)*1.0))
                        tmax = max(tmax,sum(rt)/(len(rt)*1.0))
                        result[flag][gitem][titem][app] = sum(rt)/(len(rt)*1.0)
                    tempf = eval(readFile(spath + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/dectedtime/firsttime/' + app)[0])
                    templ = eval(readFile(spath + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/dectedtime/lasttime/' + app)[0])
                    tempa = eval(readFile(spath + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/dectedtime/averagetime/' + app)[0])
                    rtime[flag][gitem][titem]['ft'][app] = tempf
                    rtime[flag][gitem][titem]['lt'][app] = templ
                    rtime[flag][gitem][titem]['at'][app] = tempa
                for i in range(len(apps)):
                    if tb[i] == tmax:
                        best[i] += 1
    fw = []
    for gitem in gn:
        temp = []
        tmax = 0
        for app in apps:
            t1 = []
            for flag in indexlist:
                subject = subjectsdict[flag]
                for titem in ts:
                    t1.append(result[flag][gitem][titem][app])
            temp.append(sum(t1)/(len(t1)*1.0))
        tmax = copy.deepcopy(temp)
        tmax.sort()
        tmax = tmax[-1]
        for i in range(len(temp)):
            if False:
                temp[i] = r'\bf{' + '%.4f' % temp[i] +'}'
            else:
                temp[i] = '%.4f' % temp[i]
        print str(gitem) + ' : ' + str(temp)
        tfw = [gitem]
        tfw.extend(temp)
        fw.append(tfw)
    print '***********************************'
    metrics = ['ft','at']
    for m in metrics:
        for gitem in gn:
            temp = []
            tmin = 0
            for app in apps:
                t1 = []
                for flag in indexlist:
                    subject = subjectsdict[flag]
                    for titem in ts:
                        t1.append(rtime[flag][gitem][titem][m][app]/(rtime[flag][gitem][titem][m][apps[-1]]*1.0))
                temp.append(sum(t1)/(len(t1)*1.0))
            tmin = copy.deepcopy(temp)
            tmin.sort()
            tmin = tmin[0]
            for i in range(len(temp)):
                if temp[i] == tmin:
                    temp[i] = r'\bf{' + '%.4f' % temp[i] +'}'
                else:
                    temp[i] = '%.4f' % temp[i]
            print str(gitem) + ' : ' + str(temp)
            tfw = [gitem]
            tfw.extend(temp)
            fw.append(tfw)
        print '***********************************'
    print '***********************************'
    for titem in ts:
        temp = []
        tmax = 0
        for app in apps:
            t1 = []
            for flag in indexlist:
                subject = subjectsdict[flag]
                for gitem in gn:
                    t1.append(result[flag][gitem][titem][app])
            temp.append(sum(t1)/(len(t1)*1.0))
        tmax = copy.deepcopy(temp)
        tmax.sort()
        tmax = tmax[-1]
        for i in range(len(temp)):
            if temp[i] == tmax:
                temp[i] = r'\bf{' + '%.4f' % temp[i] +'}'
            else:
                temp[i] = '%.4f' % temp[i]
        print str(titem) + ' : ' + str(temp)
        tfw = [titem]
        tfw.extend(temp)
        fw.append(tfw)
    print '***********************************'
    f = open('tables/rq2','w')
    for item in fw:
        f.write('\t' + str(item[0]))
        for i in item[1:]:
            f.write('& ' + i)
        f.write(r'\\' + '\n')
    f.close() 
    print indexlist

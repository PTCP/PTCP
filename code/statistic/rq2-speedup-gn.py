import os
import numpy
import copy
from collections import defaultdict

def tree(): return defaultdict(tree)

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()

def getAverage(content):
    for i in range(len(content)):
        content[i] = eval(content[i])
    return sum(content)/(len(content) * 1.0)

if __name__ == '__main__':
    path = '../../subjects/'
    subjects = readFile(path + 'uselist-gnadd-all')
    apps = ['greedytotal_withouttime.txt','greedyadditional_withouttime.txt','genetic_withouttime.txt','arp_withouttime.txt','greedytotal_withtime.txt','greedyadditional_withtime.txt','genetic_withtime.txt','arp_withtime.txt','random']
    result = defaultdict(tree)
    gn = [4,50,100,200]
    ts = [1.5]
    fw = []
    tosem_path = 'testmethod/dynamic'
    gran = 'state'
    for subject in subjects:
        spath = path + subject + '/' + tosem_path + '/'
        for gitem in gn:
            for titem in ts:
                tb = [0]*len(apps)
                tmax = 0
                for i in range(len(apps)):
                    app = apps[i]
                    if True:
                        tempf = eval(readFile(spath + gran + '/' + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/dectedtime/firsttime/' + app)[0])
                        tempa = eval(readFile(spath + gran + '/' + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/dectedtime/averagetime/' + app)[0])
                        result[subject][gitem][titem]['ft'][app] = tempf
                        result[subject][gitem][titem]['at'][app] = tempa
    metrics = ['ft','at']
    texfile = []

    print('computing resource :')
    for m in metrics:
        texstr = ''
        for gitem in gn[1:]:
            if gitem == 4:
                tempstr = r'\multirow{3}*{$\vartheta %s$} & %s'%(m.upper(),gitem)
            else:
                tempstr = '\t' + r'~ &%s'%gitem
            speeduplist = []
            for app in apps:
                speeduplist.append([])
            for titem in ts:
                for subject in subjects:
                    for i in range(len(apps)):
                        tempratio = 1- result[subject][gitem][titem][m][apps[i]]/(result[subject][4][titem][m][apps[i]] * 1.0)
                        speeduplist[i].append(tempratio)
            for i in range(len(apps)):
                tempvalue = sum(speeduplist[i])/(len(speeduplist[i])*1.0)
                if tempvalue > 0:
                    arrow = '$\uparrow$'
                else:
                    arrow = '$\downarrow$'
                tempstr += '&%.2f'%(tempvalue)
            tempstr += r'\\' + '\n'
            print('%s - %s : %s'%(m,gitem,tempstr))
            texstr += tempstr
        print(texstr)
        print('************')
    
    print('time constraint : ')
    for m in metrics:
        texstr = ''
        for titem in ts[1:]:
            #print(titem)
            if titem == 1.5:
                tempstr = r'\multirow{2}*{$\vartheta %s$} & %s'%(m.upper(),titem)
            else:
                tempstr = '\t' + r'~ &%s'%titem
            speeduplist = []
            for app in apps:
                speeduplist.append([])
            for gitem in gn:
                for subject in subjects:
                    for i in range(len(apps)):
                        tempratio = 1- result[subject][gitem][titem][m][apps[i]]/(result[subject][gitem][1.5][m][apps[i]] * 1.0)
                        speeduplist[i].append(tempratio)
            for i in range(len(apps)):
                tempvalue = sum(speeduplist[i])/(len(speeduplist[i])*1.0)
                if tempvalue > 0:
                    arrow = '$\uparrow$'
                else:
                    arrow = '$\downarrow$'
                tempstr += '&%.2f'%(tempvalue)
            tempstr += r'\\' + '\n'
            print('%s - %s : %s'%(m,titem,tempstr))
            texstr += tempstr
        print(texstr)
        print('************')

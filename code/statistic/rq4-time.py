import os
import numpy as np
from collections import defaultdict

def tree(): return defaultdict(tree)

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()


if __name__ == '__main__':
    path = '../../subjects/'
    subjects = readFile(path + 'uselist-all')
    apps = ['greedytotal_withouttime.txt','greedyadditional_withouttime.txt','genetic_withouttime.txt','arp_withouttime.txt','greedytotal_withtime.txt','greedytotal_withtime.txt','greedyadditional_withtime.txt','genetic_withtime.txt','arp_withtime.txt']
    gn = [4,8,12,16]
    tc = [1.25,1.5,1.75,2.0]
    result = tree()
    for subject in subjects:
        subject_path = path + subject + '/testmethod/dynamic/state/'
        for g in gn:
            for t in tc:
                for app in apps:
                    #print(app.rstrip('.txt'))
                    temp_time = eval(readFile(subject_path + str(t) + 'avg-new/group' + str(g) + '/time' + app[0:-4])[0])
                    result[subject][g][t][app] = temp_time
    for t in tc:
        print('%s ***********'%t)
        for g in gn:
            print('%s : '%g)
            app_list = []
            for app in apps:
                temp_list = []
                for subject in subjects:
                    temp_list.append(result[subject][g][t][app])
                app_list.append('%.2f'%np.mean(temp_list))
                #print('%s : %.2f'%(app,np.mean(temp_list)))
                del temp_list
            print(' & '.join(app_list))
            print(' --------- ')
    for app in apps:
        temp_list = []
        for t in tc:
            for g in gn:
                for subject in subjects:
                    temp_list.append(result[subject][g][t][app])
        print('%s : %s'%(app,np.mean(temp_list)))
        del temp_list
    
    f = open('timecost-all.csv','w')
    f.write('subject,gn,tc,UGT,UGA,UGE,UARP,AGT,AGA,AGE,AARP\n')
    for subject in subjects:
        for t in tc:
            for g in gn:
                temp_list = [subject,str(g),str(t)]
                for app in apps:
                    temp_list.append(str(result[subject][g][t][app]))
                f.write(','.join(temp_list) + '\n')
    f.close()

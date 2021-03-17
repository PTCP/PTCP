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
    path  = '../../subjects/'
    subjects = readFile(path + 'uselist-testclass')
    g = 4
    tc = 1.5
    result = tree()
    apps = ['greedytotal_withouttime.txt','greedyadditional_withouttime.txt','genetic_withouttime.txt','arp_withouttime.txt','greedytotal_withtime.txt','greedyadditional_withtime.txt','genetic_withtime.txt','arp_withtime.txt','random']
    for subject in subjects:
        subject_path = path + subject + '/testclass/'
        for app in apps:
            if app != 'random':
                temp_apfdc = eval(readFile(subject_path + str(tc) + 'avg-new/evaluate/' + str(g) + '/apfdc_total/' + app)[0])
            else:
                temp_list = []
                for i in range(50):
                    temp_list.append(eval(readFile(subject_path + str(tc) + 'avg-new/evaluate/' + str(g) + '/apfdc_total/' + app + str(i) + '.txt')[0]))
                temp_apfdc = np.mean(temp_list)
            temp_ft = eval(readFile(subject_path + str(tc) + 'avg-new/evaluate/' + str(g) + '/dectedtime/firsttime/' + app)[0])
            temp_at = eval(readFile(subject_path + str(tc) + 'avg-new/evaluate/' + str(g) + '/dectedtime/averagetime/' + app)[0])
            result[subject][g][tc][app]['apfdc'] = temp_apfdc
            result[subject][g][tc][app]['ft'] = temp_ft
            result[subject][g][tc][app]['at'] = temp_at
    metrics = ['apfdc','ft','at']
    labels = ['ugt','uga','uge','uarp','agt','aga','age','aarp','random']
    for metric in metrics:
        print('metric : ' + metric)
        f = open('data_rq3/%s_testclass.csv'%metric,'w')
        tempstr = ''
        for app_index in range(len(apps)):
            app = apps[app_index]
            tempstr = tempstr + '%s,'%labels[app_index]
        f.write(str(tempstr[0:-1]) + '\n')
        for subject in subjects:
            tempstr = ''
            for app in apps:
                tempstr = tempstr + '%s,'%(result[subject][g][tc][app][metric])
            f.write(str(tempstr[0:-1]) + '\n')
        f.close()
        for app in apps:
            templist = []
            for subject in subjects:
                templist.append(result[subject][g][tc][app][metric])
            if metric == 'apfdc':
                print(app + ' : %.4f'%np.mean(templist))
            else:
                print(app + ' : %.2f'%np.mean(templist))
        print('**************') 



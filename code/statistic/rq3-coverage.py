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

    coverage = ['dynamic/state','dynamic/method','callgraph/state','callgraph/method']
    apps = ['greedytotal_withouttime.txt','greedyadditional_withouttime.txt','genetic_withouttime.txt','arp_withouttime.txt','greedytotal_withtime.txt','greedyadditional_withtime.txt','genetic_withtime.txt','arp_withtime.txt','random']
    g = 4
    t = 1.5 
    result = tree()
    for cov in coverage:
        scale = []
        for subject in subjects:
            subject_path = path + subject + '/testmethod/' + cov + '/'
            for app in apps:
                if app!='random':
                    temp_apfdc = eval(readFile(subject_path + str(t) + 'avg-new/evaluate/' + str(g) + '/apfdc_total/' + app)[0])
                    temp_ft = eval(readFile(subject_path + str(t) + 'avg-new/evaluate/' + str(g) + '/dectedtime/firsttime/' + app)[0])
                    temp_at = eval(readFile(subject_path + str(t) + 'avg-new/evaluate/' + str(g) + '/dectedtime/averagetime/' + app)[0])
                else:
                    temp_list = []
                    for i in range(50):
                        temp_list.append(eval(readFile(path + subject + '/testmethod/dynamic/state/' + str(t) + 'avg-new/evaluate/' + str(g) + '/apfdc_total/' + app + str(i) + '.txt')[0]))
                    temp_apfdc = np.mean(temp_list)
                    temp_ft = eval(readFile(path + subject + '/testmethod/dynamic/state/' + str(t) + 'avg-new/evaluate/' + str(g) + '/dectedtime/firsttime/' + app)[0])
                    temp_at = eval(readFile(path + subject + '/testmethod/dynamic/state/'  + str(t) + 'avg-new/evaluate/' + str(g) + '/dectedtime/averagetime/' + app)[0])
                result[cov][subject][g][t][app]['apfdc'] = temp_apfdc
                result[cov][subject][g][t][app]['ft'] = temp_ft
                result[cov][subject][g][t][app]['at'] = temp_at
                del temp_apfdc
                del temp_at
                del temp_ft
    metrics = ['apfdc','ft','at']
    cov_label = ['dyn-statement','dyn-method','sta-statement','sta-method']
    labels = ['UGT','UGA','UGE','UARP','AGT','AGA','AGE','AARP','RANDOM']
    for cov_index in range(len(coverage)):
        cov = coverage[cov_index]
        print(cov + ' ************')
        for metric in metrics:
            temp_app_value = []
            f = open('data_coverage/%s-%s.csv'%(cov_label[cov_index],metric),'w')
            f.write(','.join(labels) + '\n')
            for subject in subjects:
                temp_list = []
                for app in apps:
                    temp_list.append('%s'%result[cov][subject][g][t][app][metric])
                f.write(','.join(temp_list) + '\n')
                del temp_list
            for app in apps:
                temp_list = []
                for subject in subjects:
                    temp_list.append(result[cov][subject][g][t][app][metric])
                if metric == 'apfdc':
                    temp_app_value.append('%.4f'%np.mean(temp_list))
                else:
                    temp_app_value.append('%.2f'%np.mean(temp_list))
            print(metric + ': ')
            print(' & '.join(temp_app_value))
            f.close()










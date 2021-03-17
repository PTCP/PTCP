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
    subjects = ['webbit','webbit_td']
    coverage = ['dynamic/state']
    apps = ['greedytotal_withouttime.txt','greedyadditional_withouttime.txt','genetic_withouttime.txt','arp_withouttime.txt','greedytotal_withtime.txt','greedyadditional_withtime.txt','genetic_withtime_dict.txt','arp_withtime.txt','random']
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
    for cov_index in range(len(coverage)):
        cov = coverage[cov_index]
        print(cov + ' ************')
        for subject in subjects:
            print(subject + ' : ')
            for metric in metrics:
                print('%s  ----------'%metric)
                temp_app_list = []
                for app in apps:
                    if metric == 'apfdc':
                        print('%s - %.4f'%(app,result[cov][subject][g][t][app][metric]))
                        temp_app_list.append('%.4f'%result[cov][subject][g][t][app][metric])
                    else:
                        print('%s - %.2f'%(app,result[cov][subject][g][t][app][metric]))
                        temp_app_list.append('%.2f'%result[cov][subject][g][t][app][metric])
                print(' & '.join(temp_app_list))
                del temp_app_list
                print('--------------')
            print('  *************************')








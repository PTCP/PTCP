import os
import numpy as np
from collections import defaultdict
import scipy.stats as stats

def tree(): return defaultdict(tree)

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()


if __name__ == '__main__':
    path_n = '../../subjects/'
    subjects = readFile(path_n + 'uselist-all')
    baseline_filelist = ['greedytotal_withouttime.txt','greedyadditional_withouttime.txt','genetic_withouttime.txt','arp_withouttime.txt','greedytotal_withtime.txt','greedyadditional_withtime.txt','genetic_withtime.txt','arp_withtime.txt','GroupTTMethod','GroupGAMethod','GroupGeneticMethod','GroupARTMethod','SAGT','GroupTAMethod','SAARP']
    gn = [4,8,12,16]
    tc = 2.0
    tosem_path = 'testmethod/dynamic'
    gran = 'state'
    result = tree()
    for subject in subjects:
        subject_path_n = path_n + subject + '/' + tosem_path + '/' + gran + '/'
        for g in gn:
            for app in baseline_filelist:
                if 'Group' in app:
                    temp_apfdc = eval(readFile(subject_path_n + str(tc) + 'avg-new/evaluate/' + str(g) + '/apfdc_total/' + app)[0])
                    temp_ft = eval(readFile(subject_path_n + str(tc) + 'avg-new/evaluate/' + str(g) + '/dectedtime/firsttime/' + app)[0])
                    temp_at = eval(readFile(subject_path_n + str(tc) + 'avg-new/evaluate/' + str(g) + '/dectedtime/averagetime/' + app)[0])
                    result[subject][g][tc][app]['apfdc'] = temp_apfdc
                    result[subject][g][tc][app]['ft'] = temp_ft
                    result[subject][g][tc][app]['at'] = temp_at
                elif app == 'SAGT':
                    temp_apfdc = eval(readFile(subject_path_n + str(20.0) + 'avg-new/evaluate/' + str(g) + '/apfdc_total/' + 'greedytotal_withtime.txt')[0])
                    temp_ft = eval(readFile(subject_path_n + str(20.0) + 'avg-new/evaluate/' + str(g) + '/dectedtime/firsttime/' + 'greedytotal_withtime.txt')[0])
                    temp_at = eval(readFile(subject_path_n + str(20.0) + 'avg-new/evaluate/' + str(g) + '/dectedtime/averagetime/' + 'greedytotal_withtime.txt')[0])
                    result[subject][g][tc]['SAGT']['apfdc'] = temp_apfdc
                    result[subject][g][tc]['SAGT']['ft'] = temp_ft
                    result[subject][g][tc]['SAGT']['at'] = temp_at
                elif app == 'SAARP':
                    temp_apfdc = eval(readFile(subject_path_n + str(20.0) + 'avg-new/evaluate/' + str(g) + '/apfdc_total/' + 'arp_withtime.txt')[0])
                    temp_ft = eval(readFile(subject_path_n + str(20.0) + 'avg-new/evaluate/' + str(g) + '/dectedtime/firsttime/' + 'arp_withtime.txt')[0])
                    temp_at = eval(readFile(subject_path_n + str(20.0) + 'avg-new/evaluate/' + str(g) + '/dectedtime/averagetime/' + 'arp_withtime.txt')[0])
                    result[subject][g][tc]['SAARP']['apfdc'] = temp_apfdc
                    result[subject][g][tc]['SAARP']['ft'] = temp_ft
                    result[subject][g][tc]['SAARP']['at'] = temp_at
                else:
                    temp_apfdc = eval(readFile(subject_path_n + str(tc) + 'avg-new/evaluate/' + str(g) + '/apfdc_total/' + app)[0])
                    temp_ft = eval(readFile(subject_path_n + str(tc) + 'avg-new/evaluate/' + str(g) + '/dectedtime/firsttime/' + app)[0])
                    temp_at = eval(readFile(subject_path_n + str(tc) + 'avg-new/evaluate/' + str(g) + '/dectedtime/averagetime/' + app)[0])
                    result[subject][g][tc][app]['apfdc'] = temp_apfdc
                    result[subject][g][tc][app]['ft'] = temp_ft
                    result[subject][g][tc][app]['at'] = temp_at
    metrics = ['apfdc','ft','at']
    for metric in metrics:
        print('metric : ' + metric)
        app_result = []
        for app in baseline_filelist:
            templist = []
            for subject in subjects:
                for g in gn:
                    templist.append(result[subject][g][tc][app][metric])
            app_result.append('%.4f'%np.mean(templist))
        print(', '.join(app_result))
        del app_result
        print('**************')

    for g in gn:
        print('%s  --------------------------'%g)
        for metric in metrics:
            app_result = []
            for app in baseline_filelist:
                templist = []
                for subject in subjects:
                    templist.append(result[subject][g][tc][app][metric])
                if metric == 'apfdc':
                    app_result.append('%.4f'%np.mean(templist))
                else:
                    app_result.append('%.2f'%np.mean(templist))
            print( metric + ' & ' + ' & '.join(app_result))
            del app_result

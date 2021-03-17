import os
import numpy as np

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()

def getAvg(items):
    count = 0
    for item in items:
        count += eval(item)
    return count/(len(items)*1.0)

if __name__ == '__main__':
    path = '../../subjects/'
    subjects = readFile(path + 'uselist-random')
    apps = ['genetic_withouttime.txt','arp_withouttime.txt','genetic_withtime.txt','arp_withtime.txt','random']
    t = 1.5
    g = 16
    for i in range(1):
        for app_index in range(len(apps)):
            app = apps[app_index]
            print('%s **********'%app)
            subject_apfdc_avg = []
            subject_ft_avg = []
            subject_at_avg = []
            subject_apfdc_std = []
            subject_ft_std = []
            subject_at_std = []
            for subject in subjects:
                subject_path = path + subject + '/testmethod/dynamic/state/'
                temp_list_apfdc = []
                temp_list_ft = []
                temp_list_at = []
                if apps[app_index] != 'random':
                    for random_inedx in range(10):
                        app = apps[app_index].rstrip('.txt') + '_%s.txt'%(random_inedx + 1)
                        temp_apfdc = eval(readFile(subject_path + str(t) + 'avg-new/evaluate/' + str(g) + '/apfdc_total/' + app)[0])
                        temp_ft = eval(readFile(subject_path + str(t) + 'avg-new/evaluate/' + str(g) + '/dectedtime/firsttime/' + app)[0])
                        temp_at = eval(readFile(subject_path + str(t) + 'avg-new/evaluate/' + str(g) + '/dectedtime/averagetime/' + app)[0])
                        temp_list_apfdc.append(temp_apfdc)
                        temp_list_ft.append(temp_ft)
                        temp_list_at.append(temp_at)
                else:
                    for random_index in range(50):
                        app = 1
                        temp_apfdc = eval(readFile(subject_path + str(t) + 'avg-new/evaluate/' + str(g) + '/apfdc_total/random%s.txt'%random_index)[0])
                        temp_ft = eval(readFile(subject_path + str(t) + 'avg-new/evaluate/' + str(g) + '/dectedtime/firsttime/randoms/random%s'%random_index)[0])
                        temp_at = eval(readFile(subject_path + str(t) + 'avg-new/evaluate/' + str(g) + '/dectedtime/averagetime/randoms/random%s'%random_index)[0])
                        temp_list_apfdc.append(temp_apfdc)
                        temp_list_ft.append(temp_ft)
                        temp_list_at.append(temp_at)
                temp_list_apfdc.sort()
                temp_list_ft.sort()
                temp_list_at.sort()
                subject_apfdc_avg.append('%.4f'%np.mean(temp_list_apfdc))
                subject_apfdc_std.append('%.4f'%np.std(temp_list_apfdc))
                subject_ft_avg.append('%.2f'%np.mean(temp_list_ft))
                subject_ft_std.append('%.2f'%np.std(temp_list_ft))
                subject_at_avg.append('%.2f'%np.mean(temp_list_at))
                subject_at_std.append('%.2f'%np.std(temp_list_at))
            print('apfdc : ')
            print('avg & ' + ' & '.join(subject_apfdc_avg) + ' & %.4f '%getAvg(subject_apfdc_avg) + r'\\')
            print('~ & ~ & STD & ' + ' & '.join(subject_apfdc_std) + r' & - \\')
            print('ft : ')
            print('avg & ' + ' & '.join(subject_ft_avg) + ' & %.2f '%getAvg(subject_ft_avg) + r'\\') 
            print('~ & ~ & STD & ' + ' & '.join(subject_ft_std) + r' & - \\')
            print('at : ')
            print('at & ' + ' & '.join(subject_at_avg) + ' & %.2f '%getAvg(subject_at_avg) + r'\\')
            print('~ & ~ & STD & ' + ' & '.join(subject_at_std) + r' & - \\')







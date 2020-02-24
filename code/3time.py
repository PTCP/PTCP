#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from xml.dom.minidom import parse
import xml.dom.minidom
import xml.etree.ElementTree as ET
from lxml.etree import Element,SubElement,tostring
import pprint
from xml.dom.minidom import parseString
import sys
from lxml import etree

'''
def readFile(filepath):
	f = open(filepath)
	content = f.read()
	f.close()
	return content.splitlines()
'''

def readFile(filepath):
        f = open(filepath)
        content = f.read()
        f.close()
        return content

def readList(filepath):
        f = open(filepath)
        content = f.read()
        f.close()
        return content.splitlines()

def sortList(temp1,temp2):
        sortedList = []
        for item in temp2:
                if item in temp1:
                        sortedList.append(item)
        return sortedList

def writeFile(filepath,content):
        f = open(filepath,'a')
        f.write(content + '\n')
        f.close()


if __name__ == '__main__':
	#path = '/devdata/zjy/subject_repository/tcp_large/'
	path = '/PTCP/subjects/source/'
	timelistener = '/PTCP/code/collect_subject/MyExecutionListener.java'
	subject_list = readList(path + 'uselist-all')
	#subject_list = os.listdir(path)
	timelist = []
	config = '''
        <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>2.22.0</version>
                <configuration>
                    <!-- exclude test case support classes -->
                    <!--excludes>
                        <exclude>org/apache/commons/mail/mocks/*</exclude>
                        <exclude>org/apache/commons/mail/settings/*</exclude>
                        <exclude>**/Abstract*Test.java</exclude>
                    </excludes-->
                    <properties>
                        <property>
                                <name>listener</name>
                                <value>MyExecutionListener</value>
                        </property>
                    </properties>
                </configuration>
            </plugin>
        '''
	#n = int(sys.argv[1])
	#for subject in subject_list[n:24+n]:
	for subject in subject_list:
		subject_path = path + subject + '/'
		os.chdir(subject_path)
		# skip multi-module subject
		if os.path.exists(subject_path + 'src/test/java') == False:
			continue
		else:
			pass
		os.system('cp -r target target_clover')
		os.system('cp ' + timelistener + ' ' + 'src/test/java/MyExecutionListener.java')
		#os.system('mkdir time')
		if os.path.exists(subject_path + 'pom.xml.ori') == False:
			os.system('cp pom.xml pom.xml.ori')
		#os.system('cp pom.xml.ori pom.xml')
		if os.path.exists(subject_path + 'time') == True:
			os.system('rm -r time')
			os.system('mkdir time')
		else:
			os.system('mkdir time')	
		
		pom = subject_path + 'pom.xml.ori'
		ns_all = etree.fromstring(readFile(pom)).nsmap
                ns = etree.fromstring(readFile(pom)).nsmap[None]
                for item in ns_all:
                        if item == None:
                                ET.register_namespace('',ns_all[item])
                        else:
                                ET.register_namespace(item,ns_all[item])
                tree = ET.parse(pom)
                print 'namespace : ' + ns
                root = tree.getroot()
                build_node = root.findall('{' + ns + '}' + 'build')[0]
		plugins_node = build_node.findall('{' + ns + '}' + 'plugins')
		plugins_node[0].append(ET.fromstring(config))
		tree.write(subject_path + 'pom.xml.time', encoding="utf-8",xml_declaration=True,method='xml')
		
		os.system('cp pom.xml.time pom.xml')

		os.system('mvn clean')
		for i in range(10):
			os.system('mvn test')
		
		timelist.append(subject)
		print subject + ' is completed!'
	'''
	f = open(path + 'timelist1','w')
	for item in timelist:
		f.write(item + '\n')
	f.close()
	'''
		

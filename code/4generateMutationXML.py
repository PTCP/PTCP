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

def readFile(filepath):
        f = open(filepath)
        content = f.read()
        f.close()
        return content


if __name__ == '__main__':
	pit = '''
	     <plugin>
                <groupId>org.pitest</groupId>
                <artifactId>pitest-maven</artifactId>
                <version>1.1.7-SNAPSHOT-MODIFY</version>
             </plugin>
	      '''
	mutationcmd = 'mvn org.pitest:pitest-maven:mutationCoverage -DtimeoutConst=8000'
	path = '/PTCP/subjects/source/'
        subject_list = os.listdir(path)
	argv_number = int(sys.argv[1])
	#for subject in subject_list[argv_number:argv_number+4]:
	for subject in subject_list:
                subject_path = path + subject + '/'
		
                pom = subject_path + 'pom.xml.ori'
                #os.system('cp ' + pom + ' ' + pom + '.clover')
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
		plugins_node[0].append(ET.fromstring(pit))
		tree.write(subject_path + 'pom.xml.mutant', encoding="utf-8",xml_declaration=True,method='xml')
		os.chdir(subject_path)
		#os.system('mvn clean test')
                os.system('cp pom.xml.mutant pom.xml')
		os.system(mutationcmd)
		
		print subject + ' is complete!'




import os
import re
import shutil
import  xml.dom.minidom
from bs4 import BeautifulSoup

SubjectRootPath = ''
ResusltRootPath = ''
prefix = ''

#xml : src file list + test file list
#source hmtl: statement sum
#test html: id and test name map
#src js: coverage matrix 
def readSubjectList(readFilePath):
	SubjectList = []
	readFile = open(readFilePath)
	for line in readFile:
		SubjectList.append(line.strip())
	readFile.close()
	return SubjectList


#main analyze function
def anaMain(xmlFilePath, subName): #loc
	global prefix
	global ResultRootPath
	TestFileList = [] # from org/apache/handoop/xxxx (no .html)
	SrcFileList = [] 
	lineList = [] #index for global start line number for each src file
	MethodLineList = []
	ConditionLineList = []
	
	#get all needs test files to be analyzied
	dom = xml.dom.minidom.parse(xmlFilePath + '/clover.xml')
	root = dom.documentElement
	testproject = root.getElementsByTagName('testproject')[0]
	testpackages = testproject.getElementsByTagName('package')
	for package in testpackages:
		testfiles = package.getElementsByTagName('file')
		for testfile in testfiles:
			testfilepath = testfile.getAttribute('path')
			if prefix not in testfilepath:
				continue
			tmpptr = testfilepath.index(prefix)
			testfilepath = testfilepath[tmpptr:]
			testfilepath = testfilepath.replace('.java', '')
			if os.path.exists(xmlFilePath + '/' + testfilepath + '.html'):
				TestFileList.append(str(testfilepath))


	#get all needs sourcefiles tobe analyzied
	dom = xml.dom.minidom.parse(xmlFilePath + '/clover.xml')
	root = dom.documentElement
	project = root.getElementsByTagName('project')[0]
	#get total line number of whole project
	#lineNum = project.getElementsByTagName('metrics')[0]
	#lineNum = int(lineNum.getAttribute('loc'))
	srcpackages = project.getElementsByTagName('package')
	UnitNum = 0
	for srcpackage in srcpackages:
		srcfiles = srcpackage.getElementsByTagName('file')
		for srcfile in srcfiles:
			srcfilepath = srcfile.getAttribute('path')
			if prefix not in srcfilepath:
				continue
			tmpptr = srcfilepath.index(prefix)
			srcfilepath = srcfilepath[tmpptr:]
			srcfilepath = srcfilepath.replace('.java', '')
			if os.path.exists(xmlFilePath + '/' + srcfilepath + '.js'):
				#print srcfilepath + ' ' + str(UnitNum)
				SrcFileList.append(str(srcfilepath))
				fileunitnum = srcfile.getElementsByTagName('metrics')[0]
				fileunitnum = int(fileunitnum.getAttribute('loc'))
				lineList.append(UnitNum)
				lines = srcfile.getElementsByTagName('line')
				for lineItem in lines:
					if str(lineItem.getAttribute('type')) == 'method':
						methodLine = int(lineItem.getAttribute('num'))
						if (UnitNum + methodLine) not in MethodLineList:
							MethodLineList.append(UnitNum + methodLine)
							#print str(methodLine) + ' ' + str(UnitNum + methodLine)
					if str(lineItem.getAttribute('type')) == 'cond':
						condLine = int(lineItem.getAttribute('num'))
						if (UnitNum + condLine) not in ConditionLineList:
							ConditionLineList.append(UnitNum + condLine)
				UnitNum = UnitNum + fileunitnum


	#map id and test name
	print(xmlFilePath)
	mapIdName = mapTest(TestFileList, xmlFilePath)
	print(TestFileList)
	
	writefile = open(ResultRootPath +'/' + subName +  '/testList', 'w')
	for item in mapIdName:
		writefile.write(item + '\n')
	writefile.close()
	
	#create 2-division array c[i][j]: test i whther cover unit j

	testSum = len(mapIdName)
	UnitSum = UnitNum
	StateCovMatrix = [[0 for col in range(UnitSum)] for row in range(testSum)]
	MethodCovMatrix = [[0 for col in range(UnitSum)] for row in range(testSum)]
	CondCovMatrix = [[0 for col in range(UnitSum)] for row in range(testSum)]
	#analyze coverage information
	FillMatrixState(StateCovMatrix, MethodCovMatrix, CondCovMatrix, SrcFileList, lineList, MethodLineList, ConditionLineList, xmlFilePath, subName, testSum, UnitSum)


def FillMatrixState(StateCovMatrix, MethodCovMatrix, CondCovMatrix, SrcFileList, lineList, MethodLineList, ConditionLineList, xmlFilePath, subName, testSum, UnitSum):
	global ResultRootPath
	filePtr = 0
	debugcount = 0
	for srcFile in SrcFileList:
		currenPtr = lineList[filePtr]
		filePtr = filePtr + 1
		#print currenPtr
		FilePath = xmlFilePath + '/' + srcFile + '.js'
		#print srcFile
		readFile = open(FilePath)
		for line in readFile:
			line = line.strip()
			if 'clover.srcFileLines = ' in line:
				line = line.replace('clover.srcFileLines = ', '')
				line = line[1:-1]
				#print line

				testItems = []
				if '],' not in line:
					testItems = testItems.append(line)
				else:
					testItems = line.split('],')
				
				
				LineItem = -1
				for testItem in testItems:
					LineItem = LineItem + 1
					testItem = testItem.strip()
					testItem = testItem.replace(']', '')
					testItem = testItem.replace('[', '')
					if testItem == '':
						continue
					#print testItem
					testIDs = testItem.split(',')
					#print testIDs
					for testID in testIDs:
						testID = testID.strip()
						testID = int(testID)
						#print 'line ' + str(LineItem)+ 'is covered by ' + str(testID)
						StateCovMatrix[testID][LineItem + currenPtr] = 1
						if (LineItem + currenPtr) in MethodLineList:
							MethodCovMatrix[testID][LineItem + currenPtr] = 1
						if (LineItem + currenPtr) in ConditionLineList:
							CondCovMatrix[testID][LineItem + currenPtr] = 1
		readFile.close()
	reacordMatrix(StateCovMatrix, ResultRootPath + '/'+ subName + '/stateMatrix.txt', testSum, UnitSum)
	reacordMatrix(MethodCovMatrix, ResultRootPath + '/'+ subName + '/methodMatrix.txt', testSum, UnitSum)
	reacordMatrix(CondCovMatrix, ResultRootPath + '/'+ subName + '/condMatrix.txt', testSum, UnitSum)

def reacordMatrix(TheMatrix, recordPath, testSum, UnitSum):
	writefile = open(recordPath, 'w')
	for i in range(0, testSum):
		for j in range(0, UnitSum):
			writefile.write(str(TheMatrix[i][j]))
		writefile.write('\n')
	writefile.close()

#map test id and test name
def mapTest(TestFileList, xmlFilePath):
	testNumber = 0
	#get test number
	for testFile in TestFileList:
		htmlPath = xmlFilePath + '/' + testFile + '.html'
		htmlFile = open(htmlPath)
		soup = BeautifulSoup(htmlFile)
		htmlFile.close()
		tdList = soup.findAll('td', {'id' : re.compile('tc-')})
		for tdItem in tdList:
			testID = str(tdItem.attrs['id'])
			testID = testID.replace('tc-', '')
			if int(testID) + 1 > testNumber:
				testNumber = int(testID) + 1

	mapIdName = []
	for i in range(0, testNumber):
		mapIdName.append('NaN')
	#print 'number ' + str(testNumber)

	for testFile in TestFileList:
		htmlPath = xmlFilePath + '/' + testFile + '.html'
		htmlFile = open(htmlPath)
		soup = BeautifulSoup(htmlFile)
		htmlFile.close()
		tdList = soup.findAll('td', {'id' : re.compile('tc-')})
		for tdItem in tdList:
			testID = str(tdItem.attrs['id'])
			testID = testID.replace('tc-', '')
			methodName = tdItem.find('span', {'class' : 'sortValue'})
			methodName = str(methodName.text)
			methodName = methodName.replace('.', '/')
			mapIdName[int(testID)] = methodName
	
	return mapIdName

# read file, return as list
def readFile(filepath):
	f = open(filepath) 
	content = f.read()
	f.close()
	return content.splitlines()

# get the prefix for subjects by analyzing dir
def getPrefix(tt):
	temp = tt
	while True:
		templist = os.listdir(temp)
		if len(templist) == 1:
			temp = temp + '/' + templist[0]
			continue
		else:
			result = temp.replace(tt,'')
			return result + '/'

if __name__ == "__main__":
	global SubjectRootPath
	SubjectRootPath = './subjects/source/'
	SubjectList = readFile(SubjectRootPath + 'uselist-all')

	for sub in SubjectList:
		#file have the handled subject list
		global ResultRootPath
		global prefix
		subject_path = SubjectRootPath + sub + '/'
		os.system('rm -r ' + subject_path + 'target_cov/')
		os.system('cp -r ' + subject_path + 'target_clover/' + ' ' + subject_path + 'target_cov/')
		
		if os.path.exists(subject_path + 'target_cov/site/clover') == False:
			print sub + ' pass'
                        continue		

		ResultRootPath = '/PTCP/subjects/experiment/' + sub + '/coverage' # anonymous processing
		if os.path.exists(ResultRootPath) == False:
			os.makedirs(ResultRootPath)
		
		# specify the prefix for some subjects, because the correct prefix can not be extracted from dir automatically
		#prefix = 'org/apache/hadoop/chukwa/'
		#prefix = 'com/tumblr/jumblr/'
		#prefix = 'org/xembly/'
		
		prefix = getPrefix(subject_path + 'src/main/java/')
		print prefix

		print 'SUBJECT ' + sub
		resultDir = ResultRootPath  + '/' + sub
		if os.path.exists(resultDir):
			shutil.rmtree(resultDir)
		os.mkdir(resultDir)
		
		anaMain(SubjectRootPath + '/' + sub + '/target_cov/site/clover', sub)

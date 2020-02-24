# PTCP
this is a simple document for all the scripts used in PTCP, including collecting dynamic and static coverage, collecting mutants, collect test dependency, running parallel test prioritization techniques, and evaluating using APFDc/FT/AT. 
	- the dir 'code/' stores the script used in this experiment, including eight parallel test prioritization techniques.
	- the dir 'subjects/experiment/' stores the data used in this experiment and the results in our study, while 
	- the dir 'subjects/source/' stores the raw data (e.g., coverage report, source code).

1. collecting dynamic coverage
	a) run python 1collect_clover.py : using clover to collect dynamic coverage.
	b) run python 1_2analyzeCoverage.py : analyzing the coverage report to get statement/method coverage.
	c) run python 1_3reducecoverage.py : creating reduced matrix for coverage matrix in order to imporve efficiency.

2. collecting static coverage
	a) run python 2collect_callgraph.py : collecting static call graph.
	b) run python 2_2analyzeCallGraph.py : analyzing the static call graph to get static statement/method coverage.

3. collecting testing time
	a) run python 3time.py.

4. collecting mutatnts
	a) run python 4generateMutationXML.py :  generating the pom.xml for PIT.
	b) run python 4_2analyzeMutant.py : collecting mutants from PIT report.
	c) run python 4_3reduceMutant.py : creating reduced matrix for mutant matrix in order to imporve efficiency.

5. collecting test dependency
	a) run python 5collect_td.py : collecting test dependency by iDFlakies.

6. collecting class-level coverage:
	a) run python 6collect_classlevel.py : get class-level coverage via method-level coverage

7. running eight parallel test prioritization techniques
	a) run each technique with parameters (e.g., run python greedytotal_withtime.py 4 1.5 testmethod/dynamic state). 
		- the first parameter is the number of computing resources e.g., 4, 8, 12, 16, 50, 100, and 200
		- the second parameter is the time constraint, e.g., 1.25, 1.5, 1.75, 2.0
		- the third parameter is test coverage and test granularity, e.g., testmethod/dynamic, testmethod/static, testclass/
		- the last parameter is the type of dynamic/static coverage, e.g., state (represents statement coverage), method
	b) the eight techniques include:
		- UGT  : greedytotal_withouttime.py
		- UGA  : greedyadd_withouttime.py
		- UGE  : genetic_withouttime.py
		- UARP : art_withouttime.py
		- AGT  : greedytotal_withtime.py
		- AGA  : greedyadd_withtime.py
		- AGE  : genetic_withtime.py
		- AARP : art_withtime.py

8. run evaluating script:
	a) run python calculate_apfd_all.py testmethod/dynamic state: calculating APFDc, the two parameters can be replaced, please refer to 7(a).
	b) run python calculate_time_all.py : calculating FT/AT, the parameters are assigned in the script.






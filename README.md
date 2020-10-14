# PTCP
This is a simple document for all the scripts used in PTCP, including collecting dynamic and static coverage, collecting mutants, collect test dependency, running parallel test prioritization techniques, and evaluating using APFDc/FT/AT.

    1. the dir 'code/' stores the scripts used in this experiment, and the dir 'code/prioritization' stores the implementation of eight parallel test prioritization techniques.
    2. the dir 'code/prioritization' stores the scripts of eight parallel test prioritization techniques.
    3. the dir 'subjects/' stores the data used in this experiment and the results in our study.
    

* collecting dynamic coverage
    * run python 1collect_clover.py : using clover to collect dynamic coverage.
    * run python 1_2analyzeCoverage.py : analyzing the coverage report to get statement/method coverage.
    * run python 1_3reducecoverage.py : creating reduced matrix for coverage matrix in order to imporve efficiency.

* collecting static coverage
    * run python 2collect_callgraph.py : collecting static call graph.
    * run python 2_2analyzeCallGraph.py : analyzing the static call graph to get static statement/method coverage.

* collecting testing time
    * run python 3time.py.

* collecting mutatnts
    * run python 4generateMutationXML.py :  generating the pom.xml for PIT.
    * run python 4_2analyzeMutant.py : collecting mutants from PIT report.
    * run python 4_3reduceMutant.py : creating reduced matrix for mutant matrix in order to imporve efficiency.

* collecting test dependency
    * run python 5collect_td.py : collecting test dependency by iDFlakies.

* collecting class-level coverage:
    * run python 6collect_classlevel.py : get class-level coverage via method-level coverage

* running eight parallel test prioritization techniques
    * run each technique with parameters, e.g., run python greedytotal_withtime.py 4 1.5 testmethod/dynamic state.
        * the first parameter is the number of computing resources e.g., 4, 8, 12, 16, 50, 100, and 200
        * the second parameter is the time constraint, e.g., 1.25, 1.5, 1.75, 2.0
        * the third parameter is test coverage and test granularity, e.g., testmethod/dynamic, testmethod/static, testclass
        * the last parameter is the type of dynamic/static coverage, e.g., state (represents statement coverage), method
    * the eight techniques include:
        * UGT  : greedytotal_withouttime.py
        * UGA  : greedyadd_withouttime.py
        * UGE  : genetic_withouttime.py
        * UARP : art_withouttime.py
        * AGT  : greedytotal_withtime.py
        * AGA  : greedyadd_withtime.py
        * AGE  : genetic_withtime.py
        * AARP : art_withtime.py

* run evaluating script:
    * run python calculate_apfd_all.py testmethod/dynamic state: calculating APFDc, the two parameters can be replaced, please refer to 7(a).
    * run python calculate_time_all.py : calculating FT/AT, the parameters are assigned in the script.
    
* the results of parallel test prioritization are stored in the dir 'subjects/'
    * TBD

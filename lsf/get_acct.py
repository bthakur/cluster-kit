#!/usr/bin/env python

import sys,os
import argparse
import pprint as pp
import re

## Re
txt_dquoted_empty='""'
txt_dquoted_triple='\s""".*"""\s'
txt_dquoted_select='"[\s]*select\[.*?"'
txt_dquoted_rusage='"*rusage\[.*?"'

#p=re.compile('[a-z]+')
com_dquotes_empty=re.compile(txt_dquoted_empty)
com_dquoted_inner=re.compile('""')
#com_dquoted_strings=re.compile
com_dquoted_select=re.compile(txt_dquoted_select)
com_dquoted_rusage=re.compile(txt_dquoted_rusage)

testline='"JOB_FINISH" "9.12" 1506309350 83758588 21583 38076563 1 1506309086 0 0 1506309290 "kleinr08" "alloc" "rusage[mem=4915] span[hosts=1]" "" "" "interactive2" "/sc/orga/scratch/kleinr08/clinseq/1/results.seqmetrics/.queueScatterGather/results.seqmetrics/.qlog/results.seqmetrics/phs000971-clinseq.1.SRR2472518.clean.dedup.recal.call.bed.callreport-sg/temp_165_of_200" "" "/sc/orga/scratch/kleinr08/clinseq/1/results.seqmetrics/.queueScatterGather/results.seqmetrics/.qlog/results.seqmetrics/phs000971-clinseq.1.SRR2472518.clean.dedup.recal.call.bed.callreport-sg/temp_165_of_200/phs000971-clinseq.1.SRR2472518.clean.dedup.recal.call.bed.out" "" "88/1506309086.83758588" 0 1 "node26-41" 64 60.0 "results_seqmetr" """exec"" ""sh"" ""/sc/orga/scratch/kleinr08/clinseq/1/results.seqmetrics/.queue.bjgWRmWswM/.exec2065393602638792977""" 38.046216'

testline='"JOB_FINISH" "9.12" 1506309350 83758588 21583 38076563 1 1506309086 0 0 1506309290 "kleinr08" "alloc" "rusage[mem=4915] span[hosts=1]" "" "" "interactive2" "/sc/orga/scratch/kleinr08/clinseq/1/results.seqmetrics/.queueScatterGather/results.seqmetrics/.qlog/results.seqmetrics/phs000971-clinseq.1.SRR2472518.clean.dedup.recal.call.bed.callreport-sg/temp_165_of_200" "" "/sc/orga/scratch/kleinr08/clinseq/1/results.seqmetrics/.queueScatterGather/results.seqmetrics/.qlog/results.seqmetrics/phs000971-clinseq.1.SRR2472518.clean.dedup.recal.call.bed.callreport-sg/temp_165_of_200/phs000971-clinseq.1.SRR2472518.clean.dedup.recal.call.bed.out" "" "88/1506309086.83758588" 0 1 "node26-41" 64 60.0 "results_seqmetr" """exec"" ""sh"" ""/sc/orga/scratch/kleinr08/clinseq/1/results.seqmetrics/.queue.bjgWRmWswM/.exec2065393602638792977""" 38.046216 1.767731 1392964 0 -1 0 0 27442 0 0 0 16 -1 0 0 0 4038 14909 -1 "notexistent" "acc_kleinr08b" 0 1 "" "" 0 1384448 0 "" "" "" "" 0 "" 0 "" -1 "/kleinr08" "" "default" "" -1 "" "" 4194320 "" 1506309290 "" "" 0 0 432000 64 886784 "select[((healthy=1)) && (type == local)] order[!-slots:-maxslots] rusage[mem=4915.00] span[hosts=1] same[model] affinity[core(1)*1] " "" -1 "" -1 0 "" 0 0 "" 60 "scratch/clinseq/1" 0 "{o;0;[0.00;node26-41(-1;/0/0/5:c:o:0;)]}" 0.000000'

testline='"JOB_FINISH" "9.12" 1506309412 83752368 21952 34930707 1 1506307743 0 0 1506309293 "rodrio10" "low" " rusage[mem=8192] span[ptile=1]" "" "mkdir -p -m 700 /dev/shm/$LSB_JOBID" "interactive1" "/sc/orga/work/rodrio10/rodrio10_projects/projects/transpac/results/2017-07-17_background/iterations/857/2" "" "/sc/orga/scratch/rodrio10/lsf-output/%J.OU" "" "368/1506307743.83752368" 0 1 "node28-14" 64 60.0 "RepeatMasker" "#!/bin/bash;#BSUB -oo /sc/orga/scratch/rodrio10/lsf-output/%J.OU;#BSUB -n 1;#BSUB -W 1:00;#BSUB -E ""mkdir -p -m 700 /dev/shm/$LSB_JOBID"";#BSUB -Ep ""rm -rf /dev/shm/$LSB_JOBID;"";#BSUB -J RepeatMasker;#BSUB -q low;#BSUB -P acc_sharpa01a;#BSUB -R span[ptile=1];#BSUB -R rusage[mem=8192];cd /sc/orga/projects/bashia02c/projects/rodrio10/projects/transpac/results/2017-07-17_background/iterations/857/2;echo -E '==> Run command    :' ""/sc/orga/work/bashia02/Thirdparty/RepeatMasker/RepeatMasker -pa 12 -species human /sc/orga/work/rodrio10/rodrio10_projects/projects/transpac/results/2017-07-17_background/iterations/857/2/50_seq_in_tsd_changed.fa"";echo    '==> Execution host :' `hostname`;export JOB_NCPUS=1;if [ -e /dev/shm/$LSB_JOBID ];then;   export TMPSHMDIR=/dev/shm/$LSB_JOBID;else;   export TMPSHMDIR=$TMPDIR;fi;/sc/orga/work/bashia02/Thirdparty/RepeatMasker/RepeatMasker -pa 12 -species human /sc/orga/work/rodrio10/rodrio10_projects/projects/transpac/results/2017-07-17_background/iterations/857/2/50_seq_in_tsd_changed.fa" 54.000000 24.762235 540444 0 -1 0 0 5768222 0 0 0 72 -1 0 0 0 3765535 643655 -1 "" "acc_sharpa01a" 0 1 "" "" 0 986112 0 "" "" "" "" 0 "" 0 "" -1 "/rodrio10" "" "default" "rm -rf /dev/shm/$LSB_JOBID;" -1 "" "" 4200464 "" 1506309293 "" "" 0 0 3600 16 460800 "select[((healthy=1)) && (type == local)] order[!-slots:-maxslots] rusage[mem=8192.00] span[ptile=1] same[model] affinity[core(1)*1] " "" -1 "" -1 0 "" 0 0 "" 122 "/sc/orga/work/rodrio10/rodrio10_projects/projects/transpac/results/2017-07-17_background/iterations/857/2" 0 "{o;0;[0.00;node28-14(-1;/0/0/3:c:o:0;)]}" 0.000000'

print 'testline'
#print testline
#testline0=com_dquotes_empty.findall(testline)
#print len(testline0)
#testline0=re.sub(txt_dquoted_empty,'DoUbLeStRiNg',testline)
#testline0=testline.replace('""', 'DoUbLeQuOtE')

sub_select=com_dquoted_select.findall(testline)
sub_rusage=com_dquoted_rusage.findall(testline)
print type(sub_select), str(sub_select)
print type(sub_rusage), str(sub_rusage)
#sys.exit()

#print testline.replace(sub_select, '_sub_select_')
#testline0=re.sub(txt_dquoted_empty,'SeLeCt',testline)
#print testline0



#testline0=com_dquotes_triple.findall(testline)
#testline0=testline.replace(' "" ', 'TrIpLeStRiNg')
#print testline0


#result=com_dquoted_inner.search(testline)
#print result
#result=p.search(testline)
#print result


parser = argparse.ArgumentParser()

parser.add_argument('-f', action='store', 
                     dest='input_file', 
                     nargs=1, help="Accounting file to be parsed")

args = parser.parse_args()
if not args.input_file:
   parser.print_help()
   sys.exit(0)

jobs_by_user={}
jobs_by_proj={}
jobs_by_wall={}
jobs_by_vmem={}

count=0
with open( args.input_file[0],'r') as fi:

     aline=fi.readline()
     print aline
     ##result=com_dquoted_inner.match(aline)
     ##print result
     ##bline=aline.replace('""','EmPtY')
     ##cline=bline.replace(' rusage','Rusage')
     ##line=shlex.split(aline)
     bline=aline.replace('""', 'DoUbLeQuOtE')
     line=aline.split()
     #print line
     while line and count<100 :
           count+=1
           #resource=[x.strip('"') for x in line[11:] if x != u'"' and x != u'""']
           #print line[0:13]
           resource=line[13:]
           #print resource
           user=line[11]  
           slots=line[6]
	   ruse=line[13]  
           tsub=line[7]
           tbeg=line[10]
	   tend=line[2]
           memory=line[-149:-148]
           project=line[-155:-154]
           partition=line[-50:-1]
	   twait=int(tbeg)-int(tsub)
	   twall=int(tend)-int(tbeg)
	   print user,project,slots,memory,tsub,tbeg,tend, twait,twall
           #print len(line),
           #print line[-174:-144],line[-155:-154]
           #pp.pprint(resource)
	   aline=fi.readline()
         # Test re
           sub_select=com_dquoted_select.findall(aline)
           sub_rusage=com_dquoted_rusage.search(aline)
           print "Select",type(sub_select), str(sub_select)
           print "Rusage",type(sub_rusage), str(sub_rusage)
         # 

           #search=re.search(com_dquoted_rusage,aline)
           #print search
           #bline=re.sub(txt_dquoted_rusage,aline,'_select_')
           #cline=bline.replace('""', 'DoUbLeQuOtE')
           
           #line=cline.split()
           #print '      '
           #print ' Beg  '
           #print   aline
           #print   line
           #print ' End  '
           #print '      '
           line=aline.split()


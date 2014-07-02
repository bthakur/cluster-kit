#!/usr/bin/env python

import sys, re
import copy
import subprocess

# Useful variables
mdiag={}
priority=[]

# Moab parameters
RESCAP=3840

# Useful re-search compilation
chr='[A-Za-z]+'
cha='[A-Za-z: ]+'
num='[-\d.]+'
nua='[-\d:. ]+'
bra='[\(]'
ket='[\)]'
sp='[\s]*'
coln='[:]'

# compile the search
u=re.compile(chr)
v=re.compile(num)
x=re.compile(chr+sp+bra+sp+cha+sp+ket)
y=re.compile(num+sp+bra+sp+nua+sp+ket)
#x=re.compile(chr+sp+bra+sp+chr+sp+coln+sp+chr+sp+ket)
#y=re.compile(num+sp+bra+sp+num+sp+coln+sp+num+sp+ket)


# functions to match title/jobdata
def findchar(strin):
    charesult=re.findall(u,strin)
    return charesult

def findnum(strin):
    numresult=re.findall(v,strin)
    return numresult

def findtitle(strin):
    titleresult=re.findall(x,strin)
    return titleresult

def findjob(strin):
    jobresult=re.findall(y,strin)
    return jobresult

# Job Id searches for number with a following  whitespace
def findid(strin):
    idresult=re.search('[\d]+\s ',strin)
    return idresult

# Parse arguments
args=sys.argv
narg=len(args)

if narg == 1:
   print args[0], "file.serv"
   sys.exit()
elif narg == 2:
   print "Using file:-", args[1]

# open file with output from mdiag -p
with open (args[1],'rb') as f:
   lines=f.readlines()

# find title/jobdata and read into list
findt=True
findw=True
ljobs=0
#jobs=defaultdict(list)
jobs=[]
jid=[]
jpr=[]
for line in lines:
    # process for title until found
    if findt:
      title=findtitle(line)
      if title and title[0][0:4] != 'info':
    #
	print '  '
	print 'Title found',title
	findt=False
	pitems=len(title)
	pvar=[[] for i in range(pitems)]
	plist=[[] for i in range(pitems)]
	pjob=[[] for i in range(pitems)]
	#print len(title), title,':'
	for item in range(pitems):
	  #print title[item][:]
	  targs=findchar(title[item][:])
	  ltargs=len(targs)
	  #print 'targs',targs, ltargs
	  for itarg in range(ltargs):
	    #print item, itarg, targs[itarg]
	    plist[item].append(targs[itarg])
	    pvar[item].append(itarg)
	    pjob[item].append(itarg)
        print '  '
        print 'Priority variables list: plist'
	print plist
        print '  '
        #sys.exit()
	#print pvar
    elif findw and not findt:
      pwlist=findjob(line)
      if pwlist:
        print '  '
        print 'Weight found', pwlist 
        #print pwlist
	for item in range(pitems):
	  wargs=findnum(pwlist[item])
          ltargs=len(wargs)
	  for itarg in range(ltargs):
            #print item, itarg, wargs[itarg]
            pvar[item][itarg]=wargs[itarg]
            #print item,itarg, pvar[item][itarg]
        findw=False
      print 'Priority variables Weights: pvar'
      print 'pvar',pvar
      print '  '

      #sys.exit()
    else:
      #print '  '
      "Procesing jobs"
      id=findid(line)
      job=findjob(line)
      if id and job:
	pr=findid(line[id.end()+1:])
        jid.append(id.group())
        jpr.append(pr.group())
        ljobs+=1
        #print 'job',ljobs,job
	#print "pr",line, jpr
	#jobs.append(ljobs)
	for item in range(pitems):
          #print "list index",item, job[item]
          wargs=findnum(job[item])
          ltargs=len(wargs)
	  #jobs[ljobs][item].append()
	  if wargs:
            for itarg in range(ltargs):
              pjob[item][itarg]=wargs[itarg]
              #print item, itarg, pjob[item][itarg]
              #pvar[item][itarg]=wargs[itarg]
	jobs.insert(ljobs,copy.deepcopy(pjob))
	#print id.group(),pr.group()
	print ljobs,pjob
	#print jobs
	#print '---'
	#jobs[ljobs][]=pjob
	#print ljobs, pjob,jobs[ljobs]
#sys.exit()


#calculation
#print jobs
#print jobs.values()
#print plist
#print pvar
#sys.exit()

# !
# ! Preprocess jobs to show interesting data
# !

# Do a top 10 waiting jobs
# Do a top 10 resource requests
# Do a top 10 jobsperuser

maxwait=0.0
maxres=0.0
jobs_qtime={}
jobs_rproc={}
for ijob in range(len(jobs)):
    job=jobs[ijob]
    #subprocess.call(["qstat",jid[ijob]])
    priority=0.0
    #print '\n', ijob, jid[ijob]
    for item in range(pitems):
      #print item, jp[item]
      for itarg in range(1,len(job[item])):
        ppart=float(job[item][itarg])*float(pvar[item][itarg])*float(pvar[item][0])
        if plist[item][itarg]=='Proc':
          res=float(job[item][itarg])
          
          jobs_rproc[str(jid[ijob])]=job[item][itarg]
          ppartc=min(RESCAP,float(job[item][itarg])*float(pvar[item][itarg]))*float(pvar[item][0])
          #print plist[item][0],'-',plist[item][itarg],':', \
          #'\t',job[item][itarg],pvar[item][itarg], pvar[item][0],'\t=',ppart,'XXX',ppartc
          ppart=ppartc
        else:
          #print plist[item][0],'-',plist[item][itarg],':', \
          #'\t',job[item][itarg],pvar[item][itarg], pvar[item][0],'\t=',ppart
          #print "This is time", plist[item][itarg]
          if plist[item][itarg] == "QTime":
             jobs_qtime[str(jid[ijob])]=job[item][itarg]
             wait=float(job[item][itarg])
             if maxwait < wait:
	       maxwait=wait
               maxwait_ijob=ijob
               #maxwait_itarg=itarg
               maxwait_jid=jid[ijob]
               #print "MaxWait Now", ijob, job[item][itarg] , maxwait
             #else:
               #print "   Wait    ", ijob, job[item][itarg] , wait
        priority+=ppart
#sys.exit()
print "============="
#print "Max wait job ", maxwait_ijob, jobs[maxwait_itarg][:]
#print "Max wait time", maxwait_ijob, jobs[maxwait_ijob][maxwait_itarg], maxwait
#print "Max wait time: Job", maxwait_ijob, jid[maxwait_ijob], maxwait
print "JobId \t JobQtime \t JobRproc"#, jobs[maxwait_ijob][:]

#for r in jid:
#  print r, '\t', jobs_qtime[str(r)], '\t', jobs_rproc[str(r)]
#  #print r, jobs_rproc[str(jid)]
#print "============="


#sys.exit()

# Calculate and show priorities
for ijob in range(len(jobs)):
    job=jobs[ijob]
    priority=0.0
    print '\n', ijob
    print 'JobID     ', jid[ijob]
    print 'Priority  ', jpr[ijob]
    print 'Parameters', plist
    print 'Weights   ', pvar
    print 'JobValues ', jobs[ijob]
    for item in range(pitems):
      #print item, jp[item]
      for itarg in range(1,len(job[item])):
	ppart=float(job[item][itarg])*float(pvar[item][itarg])*float(pvar[item][0])
	if plist[item][itarg]=='Proc':
	  ppartc=min(RESCAP,float(job[item][itarg])*float(pvar[item][itarg]))*float(pvar[item][0])
	  print plist[item][0],'-',plist[item][itarg],':', \
          '\t',job[item][itarg],pvar[item][itarg], pvar[item][0],'\t=',ppart,'XXX',ppartc
	  ppart=ppartc
	else:
          print plist[item][0],'-',plist[item][itarg],':', \
          '\t',job[item][itarg],pvar[item][itarg], pvar[item][0],'\t=',ppart

	priority+=ppart
    
	#print item,itarg,jp,jp[item][itarg], pvar[item][itarg]
	#print plist, plist[item][itarg]
        #print pvar, pvar[item][itarg]
	#print job, jp[item][itarg]
    print '\t--------'
    print '\tmdiag known Priority\t=',jpr[ijob]
    print '\tCalculated  Priority\t=',priority
    #sys.exit()

print "Maxwaiting job", maxwait_jid, maxwait

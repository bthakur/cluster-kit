#!/usr/bin/env python

import sys
import re
import copy
import time
import subprocess
import socket
import xml.dom
from xml.dom.minidom import parse, parseString

args=sys.argv
nargs=len(args)

if nargs == 1:
  comm=['pbsnodes','-x']
  p=subprocess.Popen(comm,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
  pbsxml,pbsnodeserr=p.communicate() # problem parsing as file, resolved with parseString
  ret=p.wait()
  if ret !=0 and pbsnodeserr != '':
    print "Error executing %s?" %comm, ret
    print "Error Mesg:"
    print pbsnodeserr
    sys.exit()
  doc=parseString(pbsxml)
else:
  print "This scripts does not need any arguments; ignoring"

nodes=doc.getElementsByTagName('Node')

nodesolo={}
nodelist=[] # could be a dictionary

time_srch=re.compile('(rectime=)([0-9]+)')
load_srch=re.compile('(loadave=)([0-9.]+)')
np_srch=re.compile('(np=)([0-9]+)')
gpus_srch=re.compile('(gpus=)([0-9]+)')
amem_srch=re.compile('(availmem=)([0-9]+kb)')
jobs_srch=re.compile('(jobs=)([0-9.a-z ]+)')
for node in nodes:
   #print '+',node.nodeName
   for child in node.childNodes:
     #print child, child.hasChildNodes
     if child.hasChildNodes != '':
     #print child.localName,'::::',child.firstChild.data
     #sys.exit()
       #print '|--',child.localName,':'#,dir(child)
       #print child.firstchild.getAttribute('data')
       #print dir(child)
       try:
         #print type(child.firstChild)
         #print child.firstChild.data
         nodesolo[str(child.nodeName)]=str(child.firstChild.data)
       except AttributeError:
         #print 'Some attribute error'
         pass 
         #data=child.firstChild.data
         #if data:
       #if child.firstChild.getAttribute('data'):
         #print "this was NoneType2", type(child.firstChild)
         #print child.firstChild.data
     #nodesolo[str(child.nodeName)]=str(child.firstChild.data)
   # Copy dictionary as a list element once complete
   nodelist+=[copy.deepcopy(nodesolo)]

#sys.exit()

TotalCores=0
nodesfree=0
nodesdown=0
nodesrunning=0
nodesoffline=0
for  n in nodelist:
  #print n['state'][0:3]
  TotalCores+=int(n['np'])
  if n['state'][0:3]=='fre': 
    nodesfree+=1
  elif n['state'][0:3]=='job':
    nodesrunning+=1
  elif n['state'][0:3]=='off':
    nodesoffline+=1
  elif n['state'][0:3]=='off':
    nodesoffline+=1
  elif n['state'][0:3]=='dow':
    nodesdown+=1
  nodestatus=n['status']
  m1=time_srch.search(nodestatus)
  m2=load_srch.search(nodestatus)
  m3=amem_srch.search(nodestatus)
  m4=gpus_srch.search(nodestatus)
  m5=jobs_srch.findall(nodestatus)
  print n['name'].ljust(12), n['state'].ljust(16),
  if m1:
    print time.strftime("%D-%H:%M", time.localtime(int(m1.groups()[1]))).ljust(16),
  if m2:
    print m2.groups()[1].ljust(4),
  if m3:
    print m3.groups()[1].ljust(4),
  if m4:
    print m4.groups()[1],
  if m5:
    #print nodestatus
    print m5[0][1]
  else:
    print ' '

TotalNodes=len(nodelist)
print '  '
print ' TotalNodes   \t %s' %TotalNodes
print ' TotalCores   \t %s' %TotalCores
print ' Free         \t %s' %nodesfree
print ' Down         \t %s' %nodesdown
print ' Running      \t %s' %nodesrunning
print ' Offline      \t %s' %nodesoffline

print ' ---------------------------------+'
print '  Cluster Occupancy(R) [Running/Total] : %s [%s %%]' %(nodesrunning,round(100.0*nodesrunning/TotalNodes,2))
#sys.exit()

time.sleep(5)
###########
# Parsing qstat -a now 
#print "TotalCores",TotalCores; sys.exit()

hst_srch=re.compile('[a-zA-Z]+')
jid_srch=re.compile('[\d]+.[a-z]+')

#print hostname
#hostname='mike.hpc.lsu.edu'
hostname=socket.gethostname()
m=hst_srch.search(hostname)
if m:
  host=hostname[m.start():m.end()]
  print "Host is ", host
else:
  print "We have problem finding hostname"
  sys.exit()

if nargs == 1:
  #print "Run the command 'qstat -a' to generate input"
  #sys.exit()
  comm=['qstat','-a']
  # issue getting lines
  p=subprocess.Popen(comm,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  lines,qstaterr=p.communicate() # problem parsing as file, resolved with parseString
  ret=p.wait()
  #ret=p.wait()
  #p=subprocess.check_call(comm)
  #type(p)
  #print p
  #print e
  #sys.exit()
  #lines=p.stdout.readlines()
  #print type(ret)
  #print p.stderr.readlines()
  if ret != 0 and qstaterr != '':
    print "Error executing qstat?", lines
    sys.exit()

  if lines == '':
    print "qstat shows no jobs? Quitting", lines
    sys.exit()

# Another way of doing things
# Author Bhupender Thakur 2014. Rights reserved
# Version 0.3
# uses re and avoids predetermined list ans slight cleanup

# Users and queues
#
users=[]
queues=[]

# Per queue stats
#
que_usrs=[]
que_usr_jobs={}
que_usr_qjob={}
que_usr_jids={}
que_usr_nodes={}
que_usr_cores={}
que_usr_queued={}
que_usr_reqnod={}
que_usr_reqcpu={}


# You have a queue: keys are checkpt,workq,: queues
# queues have users: que_usrs

#print lines.split('\n')[1]
#sys.exit()
a=re.compile('[\d]+.[a-z]+')
for line in lines.split('\n'):
  m=jid_srch.search(line)
  print line
  #sys.exit()
  if m:
    job=[l for l in line.split()]
    jid=job[0]
    usr=job[1]
    que=job[2]
    #nod=job[5]
    #cpu=job[6]
    stt=job[9]
    try:
       nod=float(job[5])
    except ValueError,err:
       #err=sys.exc_info()[0]
       #print err
       #print nod
       #print type(nod)
       #sys.exit()
       nod=0
    try:
       cpu=float(job[6])
    except ValueError,err:
       cpu=0
    # Parse running vs queued:
    if que not in queues:
      queues+=[que]
    if usr not in users:
      users += [usr]
    #
    que_usr=que+'_'+usr
    #
    if (que,usr) not in que_usrs:
      que_usrs+=[(que,usr)]

    #
    if que_usr in que_usr_jids:
      if stt == 'R':
        #print stt
        if que_usr in que_usr_jobs:
          que_usr_jids[que_usr]  += [jid]
          que_usr_jobs[que_usr]  += 1
          #if type(nod) == 'int':
          que_usr_nodes[que_usr] += [float(nod)]
          que_usr_cores[que_usr] += [float(cpu)]
        else:
          que_usr_jids[que_usr]  = [jid]
          que_usr_jobs[que_usr]  = 1
          que_usr_nodes[que_usr] = [float(nod)]
          que_usr_cores[que_usr] = [float(cpu)]
      elif stt == 'Q':
        if que_usr in que_usr_queued:
          que_usr_queued[que_usr]+= [jid]
          #if type(nod) == 'int':
          que_usr_reqnod[que_usr]+= [float(nod)]
          que_usr_reqcpu[que_usr]+= [float(cpu)]
        else:
          que_usr_queued[que_usr]= [jid]
          que_usr_reqnod[que_usr]= [float(nod)]
          que_usr_reqcpu[que_usr]= [float(cpu)]
    else:
      que_usr_jids[que_usr]  = [jid]
      if stt == 'R':
        print stt
        print line
        # carver bug with "--" for  NDS   TSK
        que_usr_jobs[que_usr]  = 1
        #if type(nod) == 'int':
        que_usr_nodes[que_usr] = [float(nod)]
        que_usr_cores[que_usr] = [float(cpu)]
      if stt == 'Q':
        #print stt
        que_usr_queued[que_usr]= [jid]
        #if type(nod) == 'int':
        que_usr_reqnod[que_usr]= [float(nod)]
        que_usr_reqcpu[que_usr]= [float(cpu)]
          

TotOcc=0.0
TotNodeOcc=0.0
for que in queues:
  print " +---------------------+"
  print " | Queue: %s  "%que
  print " +---------------------+"
  print "\t User \t Stat \t Jobs \t Nodes \t Tasks"

  #if que is 'bigmemtb':
  #   ppn=40
  #else:
  #   ppn=16
  AvgPpn=TotalCores/TotalNodes

  occupancy=0.0
  nodeoccupancy=0.0
  queued=0.0
  for usr in users:
    queusr=que+'_'+usr
    if str(que+'_'+usr) in que_usr_jobs:
      print "\t %s R \t %s \t %s\t %s \t" \
      %(usr.ljust(10), \
      que_usr_jobs[queusr], \
      sum(que_usr_nodes[queusr]), \
      sum(que_usr_cores[queusr]) )

      #print "\t ", usr
      #print "\t #UserJobsNodesCores      ", usr, que_usr_jobs[queusr],
      #print "\t #UserNodes     ", usr, sum(que_usr_nodes[queusr]),
      #print "\t #UserCores     ", usr, sum(que_usr_cores[queusr])
      #print "\t UserNodeCount ", que_usr_nodes[queusr]
      #print "\t UserCoreCount ", que_usr_cores[queusr]
      occupancy += sum(que_usr_cores[queusr]) #/AvgPpn
      nodeoccupancy += sum(que_usr_nodes[queusr])
    if queusr in que_usr_queued:
      print "\t %s Q \t %s \t %s \t %s" \
      %(usr.ljust(10), \
      len(que_usr_queued[queusr]), \
      sum(que_usr_reqnod[queusr]), \
      sum(que_usr_reqcpu[queusr])),\
      que_usr_jids[queusr]

      queued    += sum(que_usr_reqcpu[queusr]) #/(AvgPpn)

      #print "\t UserJobQueued ", que_usr_queued[queusr]
      #print "\t #UserCoresReq  ", usr, sum(que_usr_reqcpu[queusr])
      #print "\t UserJobIds    ", que_usr_jids[queusr]
  TotOcc+=occupancy
  TotNodeOcc+=nodeoccupancy
  print ' \t ----------------------'
  print ' \t Queued       [+=Cores/ppn] : %s' %queued
  print ' \t Occupancy(R) [+=Cores/ppn] : %s' %nodeoccupancy
  #print ' \t '

print '  '
print ' ----------------------------------+'
print '  Cluster Average ppn  Cores/Nodes : %s' %(AvgPpn)
print '  Cluster Occupancy(R) Nodes/Total : %s [%s %%]' %(TotNodeOcc,round(100.0*TotNodeOcc/TotalNodes,2))
print '  '

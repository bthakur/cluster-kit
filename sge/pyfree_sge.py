#!/usr/bin/env python

# scrapped from pyfree

import sys
import math
import getopt
import re
import copy
import time
import subprocess
import xml.dom
from xml.dom.minidom import parse, parseString


element_node='Node'	# Basic node of pbsnodes xml output

# Torque
# Only for debugging: Arguments overwritten by input
args=['-s','status','-n','mike[001-130,210,343]',\
      '-u','foo1,foo2','-u','foo3','-f','file',\
      '-u','user','-j','jobid1,jobid2', '-j', 'jobid3']

## Sge/Uge
scheduler='sge'
# sge schema is here
# https://raw.githubusercontent.com/gridengine/gridengine/master/source/dist/util/resources/schemas/qhost/qhost.xsd

#sheduler='tm'

# Options to be parsed
opts='-f:-u:-s:-j:-n:-h'

#----------------------------
# Compile useful re searches
#----------------------------
#
# For parsing name,state and status 
np_srch=   re.compile('(np=)([0-9]+)') #-Processors
gpus_srch= re.compile('(gpus=)([0-9]+)') #-GPUs
time_srch= re.compile('(rectime=)([0-9]+)') #-Recent Time
load_srch= re.compile('(loadave=)([0-9.]+)') #-Node Load
jobs_srch= re.compile('(jobs=)([0-9.a-z ]+)') #-Node Jobs
amem_srch= re.compile('(availmem=)([0-9]+)([a-zA-Z]b)') #-Avail Mem
pmem_srch= re.compile('(physmem=)([0-9]+)([a-zA-Z]b)') #-Phys Mem
tmem_srch= re.compile('(totmem=)([0-9]+)([a-zA-Z]b)') #-Total Mem
gpu_usrch= re.compile('gpu_utilization=([0-9]+%)')
gpu_msrch= re.compile('gpu_memory_utilization=([0-9]+%)')
# For parsing hostlist passed via '-n'
hname_srch      = re.compile('[a-zA-Z]+') # Hostname
intvl_srch      = re.compile(':([0-9]+)') # Interval
solo_node_srch  = re.compile('[0-9]+')    # Single node
nodes_list_srch = re.compile('[0-9,-:]+') # Block of nodes
split_nodes_srch= re.compile('([0-9]+)-([0-9]+)') # Comma sep. block

helptext="""
+-------+
| Usage :
+-------+
                    
  python  -n host[001-020:2,101-120:3,202,430]
               Run pbsnodes on 001 though 003 at intervals of 2
               Run pbsnodes on 101 though 120 at intervals of 3
               and additionally on comma separated values 202,430

  python       Without arguments, it runs pbsnodes on all nodes

  python  -h   Will print help message and exit

"""
def help():
    print helptext

# +------------------------------------------------
# ! Scan nodes:
# !   -n host[001-100:10,113]
# !   will scan host001,host011,...,host091,host113
# +------------------------------------------------
def process_nodes(a):
  # +--------------------------------
  # ! Transforms hosts to a flat list
  # +--------------------------------
  m0=hname_srch.search(a)
  cluster=a[m0.start():m0.end()]
  m1=nodes_list_srch.search(a)
  nodelist=a[m1.start():m1.end()]
  b=[]
  if m1:
    for x in nodelist.split(','):
      m2=split_nodes_srch.search(x)
      if m2:
        begin=m2.groups()[0]
	end=m2.groups()[1] if m2.groups()[1] else begin
        m4=intvl_srch.search(x)
        #print begin,end,x[m4.start()+1:m4.end()]
        intvl=int(x[m4.start()+1:m4.end()]) if m4 else 1
        pow=int(math.log(int(begin),10))
        for y in range(int(begin) ,int(end)+1,intvl):
          pow=int(math.log(y,10))+1
          node=cluster+begin[0:len(begin)-pow]+str(y)
          b.insert(0,str(node))
      else:
        m3=solo_node_srch.search(x)
        #print 'solo',m3
        if m3:
          node=cluster+x[m3.start():m3.end()]
          b.insert(0,node)
  if b==[]:
    print "No useful nodes found with -n "
  # sys.exit()
  return b


#----------------------------
# Parse Input:  getopt
#----------------------------
#
if sys.argv:
  args=sys.argv[1:]

optlist,arglist=getopt.getopt(args,opts)
#print optlist
print "Options Supplied \n %s" %optlist

opts_dic={}

for o,a in optlist:
  if o=='-u':
    if o in opts_dic:
      opts_dic[o]+=a
    else:
      opts_dic[o]=[a]
    print "User   search %s" %a
  elif o=='-j':
    print "Jobid  search %s" %a
    if o in opts_dic:
      opts_dic[o]+=[a]
    else:
      opts_dic[o]=[a]
  elif o=='-n':
    b=process_nodes(a)
    if o in opts_dic:
      opts_dic[o]+=b
    else:
      opts_dic[o]=b
    #print "Scanning Nodes \n %s " %(opts_dic[o])
    #sys.exit()
  elif o=='-s':
    print "Status search %s" %a
    if o in opts_dic:
      opts_dic[o]+=[a]
    else:
      opts_dic[o]=[a]
  elif o=='-f':
    print "Using file    %s" %a
    if o in opts_dic:
      opts_dic[o]+=[a]
    else:
      opts_dic[o]=[a]
  elif o=='-h':
    help()
    sys.exit()
  else:
    print "Unrecognized option %s" %a

nodelist=[]
#print opts_dic['-n']
if '-n' in opts_dic:
  nodelist.extend(opts_dic['-n'])
elif '-u' in opts_dic:
  print "ToDo: Union of n and u"
elif '-j' in opts_dic:
  print "ToDo: Union of n, u and"


#-------------------------------------------
# System command to get output from pbsnodes
#-------------------------------------------  
#
if scheduler == 'tm':
  comm=['pbsnodes','-x']
elif scheduler == 'sge':
  comm=['qhost','-j','-q', '-xml']
else:
  print "scheduler unknown"
  sys.exit()
  
comm.extend(nodelist)

print "Executing Command \n %s" %comm

try:
    p=subprocess.Popen(comm,stdout=subprocess.PIPE, \
                          stderr=subprocess.PIPE)
except OSError:
    print comm, "command not found"
    print " exiting ... "
    sys.exit()

pbsnodesout,pbsnodeserr=p.communicate() 
ret=p.wait()
#sys.exit()

if ret !=0 and pbsnodeserr != '':
    print "+------------------"
    print "Error executing    "
    print "+------------------"
    print comm
    print "+ Error Mesg:"
    print "+------------------"
    print pbsnodeserr
    sys.exit()

#-------------------------------------------
# Parse xml info to get data
#-------------------------------------------  
#
# Parses string with pbsnodes output into doc
doc=parseString(pbsnodesout)
nodes=doc.getElementsByTagName(element_node)
#
nodesolo={} # Dictionary for each node
nodelist=[] # Full list of nodes
#------------------------------
# Loop over nodes, copy data
#------------------------------
for node in nodes:
   nodesolo={}
   for child in node.childNodes:
     try:
       nodesolo[str(child.nodeName)]=str(child.firstChild.data)
     except AttributeError:
       pass
   # Copy dictionary as a list element once complete
   nodelist+=[copy.deepcopy(nodesolo)]
i=0
for node in nodelist:
  i=i+1
  print i
  print node
  print " "
sys.exit()
#print opts_dic

#-----------------------------
# Process nodelist from hereon
#-----------------------------
#
nodesfree=0
nodesdown=0
nodesrunning=0
nodesoffline=0

#print "Node, State, Time, Load, Memory, GPU-load GPU-Memusage, Jobs"
print "Node, State, RecTime(mins), Load, Avail-Mem, If_any[GPU-load GPU-Memusage], Jobs"

# Parse each node entry
for  n in nodelist:
  #print n
  if n['state'][0:3]=='fre': 
    nodesfree+=1
  elif n['state'][0:3]=='job':
    nodesrunning+=1
  elif n['state'][0:3]=='off':
    nodesoffline+=1
  elif n['state'][0:3]=='dow':
    nodesdown+=1
  #
  # Node name and state
  print n['name'].ljust(12), n['state'].ljust(14),
  # Begin status check if available
  if 'status' in n:
    nodestatus=n['status']
  ##
    m1=time_srch.search(nodestatus)
    m2=load_srch.search(nodestatus)
    m30=amem_srch.search(nodestatus)
    m31=tmem_srch.search(nodestatus)
    m32=pmem_srch.search(nodestatus)
    m4=gpus_srch.search(nodestatus)
    m5=jobs_srch.findall(nodestatus)
  # Recording Time
    if m1:
     print "{0:.2} \t".format((int(time.time())-int(m1.groups()[1]))/60.0) ,
  # Load
    if m2:
      print "{0:.3} \t".format(m2.groups()[1]),
  # Memory Usage: Sam's formula
    if m30:
      mem=float(m30.groups()[1]) -float(m31.groups()[1])+ \
          float(m32.groups()[1])
      if m30.groups()[2].endswith('kb'):
        mem=mem/(1024.*1024.)
        print "{0:.4}G".format(mem),
      else:
        print mem,m30.groups()[2],
  # GPUs if any:
    if m4:
      print " \t %s"%(m4.groups()[1]),
  # GPU status
    if 'gpus' in n:
      ngpus=n['gpus']
      if ngpus > 0:
        print " %s" %ngpus,
        if 'gpu_status' in n:
          g1=gpu_usrch.findall(n['gpu_status'])
          g2=gpu_msrch.findall(n['gpu_status'])
          print g1[:], g2[:],
      else:
        ngpus=0
        print "None",
  # Running Jobs
    if m5:
      print "\t %s" %m5[0][1]
    else:
      print ' '
  else:
   print ' '
  # End of status

TotalNodes=len(nodelist)
print '  '
print ' Total   \t %s' %TotalNodes
print ' Free    \t %s' %nodesfree
print ' Down    \t %s' %nodesdown
print ' Running \t %s' %nodesrunning
print ' Offline \t %s' %nodesoffline
print ' ---------------------------------+'
print ' Usage   \t %s %%' %("{0:.4}".format(100.0*nodesrunning/ TotalNodes))

print ' ---------------------------------+'
#print '  Cluster Occupancy(R) [Cores/16] : %s [%s %%]' %(TotOcc,round(100.0*TotOcc/TotNodes,2))




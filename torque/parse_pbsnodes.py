#!/usr/bin/env python
#
#---------------------------------------------------------
# Python script to parse output from `pbsnodes -x`
# This uses the output from pbsnodes in xml format and
# parses it using monidom.
#
# Required modules include:
#	re : regular expressions ()
#	xml.dom: Document Object Model API
# In RHEL 6.5 they are packaged into 
#	python-libs-2.6.6-52.el6.x86_64
#
# Bhupender Thakur HPC@LSU
#---------------------------------------------------------
#
#------------------------
# Check Modules
#------------------------
# Check for needed modules 

#-------------------------
# Required Python modules
#-------------------------
#
import sys
import re
import copy
import time
import subprocess
import xml.dom
from xml.dom.minidom import parse, parseString

#----------------------------
# Other useful input
#----------------------------
element_node='Node'	# Basic node of pbsnodes xml output

#----------------------------
# Compile useful re searches
#----------------------------
#
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

#----------------------------
# Parse Input:  No getopt
#----------------------------
#
args=sys.argv
nargs=len(args)
#
helptext="""
+-------+
| Usage :
+-------+
Without arguments                     
     python %s

With file( output from `pbsnodes -x`)
     python %s file
"""
def help():
    print helptext %(args[0],args[0])

if nargs == 1:
  #-------------------------------------------
  # System command to get output from pbsnodes
  #-------------------------------------------
  comm=["pbsnodes","-x"]
  #
  try:
    p=subprocess.Popen(comm,stderr=subprocess.PIPE, \
                          stdout=subprocess.PIPE)
  except OSError:
    print "`pbsnodes` command not found"
    print " exiting ... "
    sys.exit()

  pbsnodesout,pbsnodeserr=p.communicate() 
  ret=p.wait()

  if ret !=0 and pbsnodeserr != '':
    print "Error executing %s?" %comm, ret
    print "Error Mesg:"
    print pbsnodeserr
    sys.exit()
  # Parses string with pbsnodes output into doc
  doc=parseString(pbsnodesout)
elif nargs == 2:
  #-------------------------------------------
  # Read pbsnodes output from a file, into doc
  #-------------------------------------------
  try:
       with open(args[1],'r') as pbsnodesout:
        # Parses file with pbsnodes output into doc
        doc=parse(pbsnodesout)
  except IOError,e_r1:
	print "Error Reading file: %s" %args[1]
 	print e_r1
        help()
	#print "Usage: %s pbsnodes-x.out" %args[0]
	sys.exit()
  except:
	print "Some other error"
        help()
	sys.exit()

#------------------------------
# Use xml parser to parse 'doc'
#------------------------------
#
nodes=doc.getElementsByTagName(element_node)

nodesolo={} # Dictionary for each mode
nodelist=[] # Full list of nodes

#------------------------------
# Loop over nodes, copy data
#------------------------------
for node in nodes:
   #print '+',node.nodeName
   nodesolo={}
   for child in node.childNodes:
     #print '|--',child.nodeName,':',child.firstChild.data
     try:
       nodesolo[str(child.nodeName)]=str(child.firstChild.data)
     except AttributeError:
       pass
   # Copy dictionary as a list element once complete
   nodelist+=[copy.deepcopy(nodesolo)]
#i=0
#for node in nodelist:
#  i=i+1
#  print i
#  print node
#  print " "
#sys.exit()
#-----------------------------
# Process nodelist from hereon
#-----------------------------
#
nodesfree=0
nodesdown=0
nodesrunning=0
nodesoffline=0

#print "Node, State, Time, Load, Memory, GPU-load GPU-Memusage, Jobs"
print "Node, State, RecTime(mins), Load, Memory, If_any[GPU-load GPU-Memusage], Jobs"

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

   

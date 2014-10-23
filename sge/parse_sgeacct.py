#!/usr/bin/env python

import os, sys
import re
import getopt
import gzip

helptext="""
+-------+
| Usage :
+-------+
                    
./parse_sgeacct.py  -b Begin_date: same as qacct
                    -e End_date: same as qacct
                    -j Use the jobid

  # This is what you would really use it for
                    -a At_this_time(Begin and End date must lie within)

  # Use accounting files(comma separated, or zipped)
                    -f  accounting-20140405,accounting-20140505.gz 

  ./parse_sgeacct.py -h  Will print help message and exit

  ./parse_sgeacct.py     Without arguments, shoud process default accounting

"""

def help():
    print helptext

#----------------------------
# SGE stuff:
#----------------------------
dir_sge_root=os.environ["SGE_ROOT"]
dir_sge_cell=os.environ["SGE_CELL"]
sge_rootcell=dir_sge_root+'/'+dir_sge_cell

dir_cur_acct='common'
dir_log_acct='log'

sge_cur_acct='accounting'
sge_cur_rept='reporting'

#print type(dir_sge_root), dir_sge_root
print type(dir_sge_cell), sge_rootcell

default_acct=sge_rootcell+'/'+dir_cur_acct+'/'+sge_cur_acct
default_rept=sge_rootcell+'/'+dir_cur_acct+'/'+sge_cur_rept

# Change if your defaut is somewhere else
# We will read default what any other file passed

#default_acct=?some_usr_global_copy

print default_acct
#sys.exit()

#----------------------------
# Files Check: sge accounting
#----------------------------

def files_to_list(f):
    mf=f.split(',')
    # Check if files exist
    g=[]
    for f in mf:
        if os.path.isfile(f) or \
           os.path.isfile(str(sge_rootcell+'/'+dir_cur_acct+'/'+f)) or \
           os.path.isfile(str(sge_rootcell+'/'+dir_log_acct+'/'+f)) :
             print "is  file",f
             g.append(f)
        else:
             print "not file",f
    if len(g)==0:
        print "None of the files could be used"
        # Use default accounting file
        g.append(default_acct)
    else:
        # Check if the files need to be unzipped
        for f in g:
            if f.endswith('.gz'):
                print "A  zipped file", f
    


#----------------------------
# Parse Input:  getopt
#----------------------------

opts='-f:-a:'
if sys.argv:
    args=sys.argv[1:]

optlist,arglist=getopt.getopt(args,opts)
print "Options Supplied \n %s" %optlist

opts_dic={}

for o,a in optlist:
  if o=='-f':
    list_of_files=files_to_list(a)
  elif o=='-a':
    print a
  elif o=='-h':
    help()
    sys.exit()

#----------------------------
# Parse Files: add files
#----------------------------

#print list_of_files


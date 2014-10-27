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
def check_sge():
    global default_acct, f_sge
    try:
      dir_sge_root=os.environ["SGE_ROOT"]
      dir_sge_cell=os.environ["SGE_CELL"]
      f_sge=True
    except KeyError:
      print "SGE_ROOT/CELL undefined, Will try reading files locally"
      f_sge=False

    if f_sge:				# With sge		
      dir_cur_acct='common'		# Def. location for accounting
      dir_log_acct='log'		# Def. location for log
      sge_cur_acct='accounting'		# Def. accounting file
      sge_cur_rept='reporting'		# Def. reporting file
      #
      sge_rootcell=dir_sge_root+'/'+dir_sge_cell
      default_acct=sge_rootcell+'/'+dir_cur_acct+'/'+sge_cur_acct
      default_rept=sge_rootcell+'/'+dir_cur_acct+'/'+sge_cur_rept
      #	
    else:				# Without sge
      dir_cur_acct=os.getcwd()          # Def. location is cwd
      dir_log_acct=os.getcwd()          # Def. location for cwd
      default_acct='accounting'
      default_rept='reporting'

  #Change if your defaut is somewhere else
  #default_acct=?some_usr_global_copy
    print default_acct

#----------------------------
# Files Check: Parse files
#----------------------------
#----------------------------
# Parse Input:  getopt
#----------------------------

def check_opts():
    global f_fopt;global f_aopt
    f_sge=False; f_fopt=False; f_aopt=False;
    print default_acct;
    opts='-f:-a:-h'
    if sys.argv:
      args=sys.argv[1:]

    optlist,arglist=getopt.getopt(args,opts)
    print "Options Supplied \n %s" %optlist

    opts_dic={}

    for o,a in optlist:
      if o=='-f':
        f_fopt=True
        list_of_files=files_to_list(a)
      elif o=='-a':
        f_aopt=True
        print a
      elif o=='-h':
        help()
        sys.exit()

  #def files_to_list(f):
    g=[]
    g+=[default_acct]
    #print type(g),default_acct,g
    if f_fopt:
      mf=f.split(',')
      # Check if files exist
      for f in mf:
        if os.path.isfile(f) or \
           os.path.isfile(str(sge_rootcell+'/'+dir_cur_acct+'/'+f)) or \
           os.path.isfile(str(sge_rootcell+'/'+dir_log_acct+'/'+f)) :
             print "is  file",f
             g.append(f)
        else:
             print "not file",f
    g=list(set(g))
    print type(g),g
    #sys.exit()
    #if len(g)==0:
    #    print "None of the files could be used"
    #    # Use default accounting file
    #    g.append(default_acct)
    #else:
    #    # Check if the files need to be unzipped
    #    for f in g:
    #        if f.endswith('.gz'):
    #            print "A  zipped file", f
    #if len(g) > 1:
    #    print "Several files need concatenation"
    #    sys.exit() 


#----------------------------
# Parse Files: add files
#----------------------------

    #print list_of_files
    a=[]
    #if a:
    for f in g:
        with open(f,'read') as fi:
            a.extend(fi.readlines())
    
    print a[0]
    print a[1]
    print a[-1]

#----------------------------
# Main
#----------------------------

def main():
    global f_sge, f_fopt, f_aopt, default_acct
    check_sge()
    check_opts() 
    #read_accounting()
    #print list_of_files

if __name__ == "__main__":
    main()



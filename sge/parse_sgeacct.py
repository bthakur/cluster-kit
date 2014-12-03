#!/usr/bin/env python

import os, sys
import re
import getopt
import gzip, bz2
import pprint as pp
import mmap
import subprocess

helptext="""
+-------+
| Usage :
+-------+
                    
./parse_sgeacct.py  -b Begin_date: same as qacct
                    -e End_date: same as qacct
                    -j Use the jobid
                    -L last job
                    -Q Pass known options to qacct
                    -a At_this_time(Begin and End date must lie within)
                    -w Running in this window(Start is before, End if after)
                    -f accounting-20140405,accounting-20140505.gz 
                       # Use accounting files(comma separated, or zipped)
./parse_sgeacct.py  -h # Will print help message and exit
./parse_sgeacct.py     # No arguments, shoud process default use qacct?

"""

def help():
    print helptext

#----------------------------
# SGE support:
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

    if  f_sge:				# With sge		
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
        default_acct=dir_cur_acct+'/'+'accounting'
        default_rept=dir_cur_acct+'/'+'reporting'

  #Change if your defaut is somewhere else
  #default_acct=?some_usr_global_copy
    print default_acct

#----------------------------
# Parse Input:  getopt
#----------------------------

def check_opts():
#-# Globals at the top
    #global f_fopt;global f_aopt, 
    global dic_arg
    f_sge=False; f_fopt=False; f_aopt=False;
    #print default_acct;
#-# Options we can parse
    opts='-f:-a:-h-Q'
    if  sys.argv:
        args=sys.argv[1:]
        optlist,arglist=getopt.getopt(args,opts)
        print "+-----------------+"
        print "| Options Supplied|"
        print "+-----------------+"
        print " %s" %optlist
        dic_arg={}
        #sys.exit()
        for o,a in optlist:
            dic_arg[o]=a
            #if o=='-f':
            #    print "Processing -f"
            #    #f_fopt=True
            #elif o=='-Q':
            #    f_Qopt=True
            #elif o=='-a':
            #    f_aopt=True
            #elif o=='-h':
            if o=='-h':
               help()
               sys.exit()
        print "dictionary",dic_arg
        #sys.exit()
#-# Read accounting files(default and passed with -f)
  #----------------------------
  # File Checks: Parse files
  #----------------------------
    g=[]
    h=[]
    acct_jobs=[]
    acct_file_list=[]
    if os.path.isfile(default_acct):
#----# Add default accounting
       g+=[default_acct]
       acct_file_list.append((default_acct,'def'))
       #print " Adding default accounting", (default_acct,'def')
#----# Check if other files provided exist
       if  '-f' in dic_arg:
           mf=dic_arg['-f'].split(',')
           #print 'f_sge',f_sge
#--------# Check SGE default directories
           if  f_sge:
               for f in mf:
                 for fullf in  \
                     sge_rootcell+'/'+dir_cur_acct+'/',+f, \
                     sge_rootcell+'/'+dir_log_acct+'/'+f:
                     if os.path.isfile(fullf):
                        g.append(fullf)
#--------# Check cwd(default) directory
           else:
               for f in mf:
                 for fullf in [os.getcwd()+'/'+str(f)] :
                     #print fullf
                     if os.path.isfile(fullf):
                        g.append(fullf)
#-# Reduce list to remove duplicates
    g=list(set(g))
    #print "    Full list",g
#-# Check if the files need to be unzipped
    for f_i in g:
        #print "----+----------------+ "
        #print "    | Parsing file : %s " %f_i
        #print "    +----------------+ "
        #print "    %s" %f_i
        f=str(f_i)
        #continue
        if f.endswith('.tar.gz'):
             fname=f[:-7]
             #comm=['gunzip',fname]   
             #print "A  zipped file", f
             # Read contents of gz file
             break
        elif f.endswith('.tar.bz2'):
             fname=f[:-8]
             break
        elif f.endswith('.tgz'):
             fname=f[:-4]
             break
        elif f.endswith('.tar.Z'):
             fname=f[:-6]
             break
        elif f.endswith('.gz'):
             fname=f[:-3]
             #print 'fname',fname
             #print 'f_i',f_i
             try:
                 with gzip.open(f_i,'rb') as fi:
                      lines=fi.readlines()
                      acct_file_list.append((fname,'gz'))
                      acct_jobs.extend(lines)
                      print "    (%s, %s)" %(fname,'gz')
                      #print acct_jobs[0]
                      #sys.exit()
             except:
                 print "Error reading file", (fname,'gz')
                 pass
        elif f.endswith('.Z'):
             fname=f[:-2]
             #comm=['zcat',fname]
             break
        elif f.endswith('.bz2'):
             fname=f[:-3]
             try:
                 h=b2.decompress(f_i)
                 with open(h,'r') as fi:
                      acct_file_list.append((fname,'bz2'))
                      acct_jobs.append(fi.readlines())
                      print "    (%s, %s)" %(fname,'bz2')
                      #print acct_jobs[0]
             except:
                 print "Error reading", (fname,'bz2')
                 #comm=['bzip2',f]
             break
        else:
             fname=f_i
             acct_file_list.append((fname,'nozip'))
             #print "    No extension, will try reading as such", (fname,'nozip')
             try:
                 with open(f_i,'r') as fi:
                      lines=fi.readlines()
                      acct_file_list.extend((fname,'nozip'))
                      acct_jobs.extend(lines)
                      print "    (%s, %s)" %(fname,'nozip')
                      #print acct_jobs[0]
             except Exception as err:
                 print err
                 #pass
#-# Reduce list to remove duplicate job entries, needless?, worth it?
    acct_jobs=list(set(acct_jobs))
    pp.pprint(acct_jobs[1:10])

#-# Read accounting files(default and passed with -f)
    #----------------------------
    # Parse option -Q: pass this assembled file/other options to qacct
    #----------------------------
    if '-Q' in dic_arg:
#----# Check if qacct is available

#---# Create memory map file
    #----------------------------
    # Pass file without wrapper options -Q, -a, -L
    #----------------------------
       mjobs=mmap.mmap(-1,13)
       mjobs= acct_jobs
       print "Mmap"
       print "========="
       print mjobs[10]
       dic_qacct={}
       print dic_arg
       for k,v in dic_arg.items():
         if k == '-Q':
            print k,v
            continue
            #dic_qacct[k]=v
         elif k == '-a':
            continue
         elif k == '-f':
            dic_qacct[k]=mjobs
         else:
            dic_qacct[k]=v
       print 'dic_qacct', dic_qacct.keys()

#---# Subprocess to run qacct command
    #----------------------------
    # Check new options
    #----------------------------
 

    #for f in g:
    #    with open(f,'read') as fi:
    #        a.extend(fi.readlines())
    #print a[0]
    #print a[1]
    #print a[-1]

#----------------------------
# Main
#----------------------------

def main():
    global f_sge, default_acct
    check_sge()
    check_opts()
    #read_accounting()
    #print list_of_files

if __name__ == "__main__":
    main()



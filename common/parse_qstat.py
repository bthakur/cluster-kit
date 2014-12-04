#!/usr/bin/env python27

import os,sys
import subprocess


# # Check Scheduler support
def check_scheduler():
    obj_sch={}
    com_qst=['which','qstat']
    try:
        p=subprocess.Popen(com_qst,stderr=subprocess.PIPE, \
                          stdout=subprocess.PIPE)
    except OSError:
        print "%s command failed" %com_qst
        print " exiting ... "
        sys.exit()

    whi_qst_out,whi_qst_err=p.communicate() 
    ret=p.wait()
    if ret !=0 and whi_qst_err != '':
        print "+------------------"
        print "Error executing    "
        print "+------------------"
        print com_qst
        print "+ Error Mesg:"
        print "+------------------"
        print whi_qst_err
        sys.exit()
    print whi_qst_out
    for sch in ['uge', 'torque', 'slurm']:
      if sch in whi_qst_out:
        obj_sch['name']=sch
        obj_sch['env']={'PATH':whi_qst_out[:-len('/qstat')-1]}
      if sch == 'uge':
        obj_sch['env']['SGE_ROOT']=''
        obj_sch['env']['SGE_CELL']=''
        print "Supports %s" %sch
    print obj_sch
#----------------------------
# Main
#----------------------------

def main():
    print "Check Scheduler"
    check_scheduler()
    #check_sge()
    #acct_jobs
    #read_accounting()
    #print list_of_files

if __name__ == "__main__":
    main()

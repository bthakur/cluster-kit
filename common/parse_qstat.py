#!/usr/bin/env python27

import os,sys
import subprocess

# # Some global definitions
global schedulers
schedulers=['uge', 'torque', 'slurm']

def check_scheduler():
    obj_sch={}
    com_qst=['which','qstat']
    obj_sch['qstat']=com_qst
    try:
        p=subprocess.Popen(com_qst,stdout=subprocess.PIPE, \
                          stderr=subprocess.PIPE)
    except:
        print "    %s command failed" %com_qst
    whi_qst_out,whi_qst_err=p.communicate() 
    ret=p.wait()
    obj_sch['err_code']=ret
    for sch in schedulers:
      if sch in whi_qst_out:
        obj_sch['name']=sch
        obj_sch['env']={'PATH':whi_qst_out[:-len('/qstat')-1]}
      else:
        obj_sch['name']=None
      if 'env' in whi_qst_out:
        if sch == 'uge':
          obj_sch['env']['SGE_ROOT']=''
          obj_sch['env']['SGE_CELL']=''
          print "Supports %s" %sch
        elif sch == 'torque':
          obj_sch['env']['PBS_HOME']=''
          obj_sch['env']['PBS_SERVER']=''
          print "Supports %s" %sch
        elif sch == 'slurm':
          obj_sch['env']['SLURM_']=''
          obj_sch['env']['SLURM_']=''
          print "Supports %s" %sch
        else:
          print "Found no supported scheduler...Exiting"
          #sys.exit()
      else:
        obj_sch['name']=None
    print '''
    Checking scheduler support %s
    Command tried              %s
    Return Error               %s
    Found support for          %s
    ''' %(schedulers, obj_sch['qstat'],obj_sch['err_code'],obj_sch['name'])
    return obj_sch
#----------------------------
# Main
#----------------------------

def main():
  # Check Scheduler
    o_sch=check_scheduler()

    #check_sge()
    #acct_jobs
    #read_accounting()
    #print list_of_files

if __name__ == "__main__":
    main()

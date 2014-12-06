#!/usr/bin/env python27

import os,sys
import subprocess
import re

# Some global definitions
global schedulers
schedulers=['uge', 'torque', 'slurm']

# Get version by running command
def get_version(com):
    print com
    try:
        p=subprocess.Popen(com,stderr=subprocess.PIPE, \
                          stdout=subprocess.PIPE,universal_newlines=True)   
    except:
        print "    %s did not return version" %com
    ret=p.wait()
    err,out=p.communicate()
    #print "Out",out
    #print "Err",err
    #print "Ret",ret
    ver=None
    if ret == 0:
        m=re.search('[\d.]+',err+out)
        print m.group(0)
        ver=m.group(0)
    return ver

# Check scheduler support
def check_scheduler():
    obj_sch={}
    com_qst=['which','qstat']
    try:
        p=subprocess.Popen(com_qst,stdout=subprocess.PIPE) #, \
        #                  stderr=subprocess.PIPE)
    except:
        print "    %s command failed" %com_qst
    whi_qst_out,whi_qst_err=p.communicate() 
    ret=p.wait()
    obj_sch['err_code']=ret
    for sch in schedulers:
      if sch in whi_qst_out:
        obj_sch['name']=sch
        obj_sch['env']={'PATH':whi_qst_out[:-len('/qstat')-1]}
        if sch == 'uge':
          obj_sch['env']['SGE_ROOT']=os.environ['SGE_ROOT']
          obj_sch['env']['SGE_CELL']=''
          obj_sch['sch_stat']=['qstat','-u','*']
          obj_sch['sch_host']=['qhost','-j']
          obj_sch['get_ver']=['-help']
          #print "Supports %s" %sch
        elif sch == 'torque':
          obj_sch['env']['PBS_HOME']=''
          obj_sch['env']['PBS_SERVER']=''
          obj_sch['sch_stat']=['qstat']
          obj_sch['sch_host']=['pbsnodes']
          obj_sch['get_ver']=['--version']
          #print "Supports %s" %sch
        elif sch == 'slurm':
          obj_sch['env']['SLURM_ROOT']=os.environ['SLURM_ROOT']
          obj_sch['env']['SLURM_']=''
          obj_sch['sch_stat']=['sinfo']
          obj_sch['sch_host']=['scontrol','show','node']
          obj_sch['get_ver']=['--version']
          #print "Supports %s" %sch
        else:
          print "Found no supported scheduler...Exiting"
          sys.exit()
        com_ver=[obj_sch['sch_stat'][0]]+obj_sch['get_ver']
        #print com_ver
        obj_sch['sch_ver']=get_version(com_ver)
    #print obj_sch
    print '''
    Checking scheduler support %s
    Command tried              %s
    Return Error               %s
    Found support for          (%s, %s)
    ''' %(schedulers, obj_sch['sch_stat'],obj_sch['err_code'],obj_sch['name'],obj_sch['sch_ver'])
    
    return obj_sch
    sys.exit()

def run_command(com_inp):
    com_out={}
    p=subprocess.Popen(com_inp,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err=p.communicate()
    print out[0]
    com_out['inp']=com_inp
    com_out['out']=out
    return com_out

#----------------------------
# Main
#----------------------------

def main():
  # Check Scheduler
    o_sch=check_scheduler()
    print o_sch['name']
    #o_qst=run_command(o_sch['sch_stat'])
    #print o_qst['out'][0]

if __name__ == "__main__":
    main()


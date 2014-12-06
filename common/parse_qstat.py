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
        obj_sch['qstat']=qstat
        obj_sch['qhost']=qstat
        obj_sch['env']={'PATH':whi_qst_out[:-len('/qstat')-1]}
      else:
        obj_sch['name']=None
      if 'env' in whi_qst_out:
        if sch == 'uge':
          obj_sch['env']['SGE_ROOT']=''
          obj_sch['env']['SGE_CELL']=''
          obj_sch['sch_stat']=['qstat','-u','*','-v']
          obj_sch['sch_host']=['qhost']
          print "Supports %s" %sch
        elif sch == 'torque':
          obj_sch['env']['PBS_HOME']=''
          obj_sch['env']['PBS_SERVER']=''
          obj_sch['sch_stat']=qstat
          obj_sch['sch_host']=pbsnodes
          print "Supports %s" %sch
        elif sch == 'slurm':
          obj_sch['env']['SLURM_']=''
          obj_sch['env']['SLURM_']=''
          obj_sch['sch_stat']=['sinfo']
          obj_sch['sch_host']=['scontrol','show','node']
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

def run_command(com_inp):
    com_out={}
    p=subprocess.Popen(com_inp,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err=p.communicate()
    print out
    com_out['inp']=com_inp
    com_out['out']=out
    com_out['ver']=
    return com_out

#----------------------------
# Main
#----------------------------

def main():
  # Check Scheduler
    o_sch=check_scheduler()
    print o_sch['name']
    o_qst=run_command(o_sch['qstat'])
    print o_qst['out']

if __name__ == "__main__":
    main()


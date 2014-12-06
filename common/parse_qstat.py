#!/usr/bin/env python27

import os,sys
import subprocess

# # Some global definitions
global schedulers
schedulers=['uge', 'torque', 'slurm']

def get_version(com):
    try:
        p=subprocess.Popen(com,stdout=subprocess.PIPE, \
                          stderr=subprocess.PIPE)
    except:
        print "    %s command failed" %com_qst
    out,err=p.communicate()
    if err != '':
        ver=out[2]
    

def check_scheduler():
    obj_sch={}
    com_qst=['which','qstat']
    #obj_sch['qstat']=com_qst
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
          obj_sch['env']['SGE_ROOT']=os.environ['SGE_ROOT']
          obj_sch['env']['SGE_CELL']=''
<<<<<<< HEAD
          obj_sch['qstat']=['qstat', '-u', '*']
          obj_sch['qhost']=['qhost', '-j']
=======
          obj_sch['sch_stat']=['qstat','-u','*']
          obj_sch['sch_host']=['qhost','-j']
          obj_sch['get_ver']=['-help']
>>>>>>> 2f73d0f3902d5a75570e9bff9ec4aca25e357fea
          print "Supports %s" %sch
        elif sch == 'torque':
          obj_sch['env']['PBS_HOME']=''
          obj_sch['env']['PBS_SERVER']=''
          obj_sch['sch_stat']=['qstat']
<<<<<<< HEAD
          obj_sch['sch_host']=pbsnodes
=======
          obj_sch['sch_host']=['pbsnodes']
          obj_sch['get_ver']=['-v']
>>>>>>> 2f73d0f3902d5a75570e9bff9ec4aca25e357fea
          print "Supports %s" %sch
        elif sch == 'slurm':
          obj_sch['env']['SLURM_ROOT']=os.environ['SLURM_ROOT']
          obj_sch['env']['SLURM_']=''
          obj_sch['sch_stat']=['sinfo']
          obj_sch['sch_host']=['scontrol','show','node']
          obj_sch['get_ver']=['-v']
          print "Supports %s" %sch
        else:
          print "Found no supported scheduler...Exiting"
          sys.exit()
        obj_sch['sch_ver']=get_version[obj_sch['sch_stat'],obj_sch['get_ver']]
      else:
        obj_sch['name']=None
      
    print '''
    Checking scheduler support %s %s
    Command tried              %s
    Return Error               %s
    Found support for          %s
    ''' %(schedulers, obj_sch['qstat'],obj_sch['sch_ver'],obj_sch['err_code'],obj_sch['name'])
    
    return obj_sch
    sys.exit()

def run_command(com_inp):
    com_out={}
    p=subprocess.Popen(com_inp,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err=p.communicate()
<<<<<<< HEAD
    print out[0]
=======
    print out
    com_out['inp']=com_inp
>>>>>>> 2f73d0f3902d5a75570e9bff9ec4aca25e357fea
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
    #print o_qst['out'][0]

if __name__ == "__main__":
    main()


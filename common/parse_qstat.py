#!/usr/bin/env python27

import os,sys
import subprocess as sp
import re
import pprint as pp

# Some global definitions
global schedulers,sched_stat, re_srch
schedulers=['sge','uge', 'torque', 'slurm']
sched_stat={'sge':'qstat','uge':'qstat','torque':'qstat','slurm':'squeue'}
#sched_sche={'sge':'qstat','uge':'.xsd','torque':'','slurm':''}

# Useful re-search compilation
re_srch={ 'jid':'job(.*?)id','sta':' s|state ','que':'queue','usr':'user'}

scm_sta=['sta','usr','jid' ]
#scm_usr=['']
scm_que=['que','usr','jid']

# Get version by running command

def run_command(com_inp):
    com_out={}
    try:
        p=sp.Popen(com_inp,stdout=sp.PIPE, stderr=sp.PIPE)
    except:
        print "    %s did not return version" %com
    # some issues on carver python26 with p.wait
    #ret=p.wait()
    out,err=p.communicate()
    com_out['ret']=p.returncode
    com_out['inp']=com_inp
    com_out['err']=err
    if p.returncode ==0 :
        com_out['out']=str.split(out,'\n')
    return com_out

def get_version(com):
    o_com=run_command(com)
    ver=None
    if o_com['ret'] == 0:
        m=re.search('[\d.]+',str(o_com['err'])+str(o_com['out']))
        ver=m.group(0)
    return ver

# Check scheduler support
def check_scheduler():
    obj_sch={}
    #
    for sch in schedulers:
      com_qst=['which',sched_stat[sch]]
      o_com=run_command(com_qst)
      if o_com['ret'] ==0:
          out=o_com['out'][0]
          obj_sch['env']={'PATH':out[:-len(sched_stat[sch])-1]}
          if 'uge' in out:
            obj_sch['env']['SGE_ROOT']=os.environ['SGE_ROOT']
            obj_sch['env']['SGE_CELL']=os.environ['SGE_CELL']
            obj_sch['sch_name']='uge'
            obj_sch['sch_stat']=['qstat','-u','*']
            obj_sch['sch_host']=['qhost','-j']
            obj_sch['sch_ver']=['-help']
            #print "Supports %s" %sch
          elif 'sge' in out:
            obj_sch['env']['SGE_ROOT']=os.environ['SGE_ROOT']
            obj_sch['env']['SGE_CELL']=os.environ['SGE_CELL']
            obj_sch['sch_name']='sge'
            obj_sch['sch_stat']=['qstat','-u','*']
            obj_sch['sch_host']=['qhost','-j']
            obj_sch['sch_ver']=['-help']
          elif 'torque' in out:
            obj_sch['env']['PBS_HOME']=''
            obj_sch['env']['PBS_SERVER']=''
            obj_sch['sch_name']='torque'
            obj_sch['sch_stat']=['qstat']
            obj_sch['sch_host']=['pbsnodes']
            obj_sch['sch_ver']=['--version']
            #print "Supports %s" %sch
          elif 'slurm' in out:
            #obj_sch['env']['SLURM_ROOT']=os.environ['SLURM_ROOT']
            obj_sch['sch_name']='slurm'
            obj_sch['sch_stat']=['squeue']
            obj_sch['sch_host']=['scontrol','show','node']
            obj_sch['sch_name']='slurm'
            obj_sch['sch_ver']=['--version']
            #print "Supports %s" %sch
          else:
            print "Found no support for %s" %sch
            #sys.exit()
          com_ver=[obj_sch['sch_stat'][0]]+obj_sch['sch_ver']
          obj_sch['sch_ver']=get_version(com_ver)
      else:
        print "Did not find", sch
        #sys.exit()
    pp.pprint(obj_sch)
    if 'sch_stat' in obj_sch:
        print '''
        Checking scheduler support %s
        Command tried              %s
        Found support for          (%s, %s)
        ''' %(schedulers, obj_sch['sch_stat'],obj_sch['sch_name'],obj_sch['sch_ver'])
    return obj_sch

def get_elements_byschema(xml_doc, xml_sche, xml_typ):
    print 'testing'
    nam_spc = xml_doc.xpath("//xsd:element[@type = $n]/@name",
                            namespaces={"xsd": 
                                        "http://www.w3.org/2001/XMLSchema"},
                            n=xml_typ)

def check_schema(sch,ver):
    ava_scm={'uge-8.1.7':''}

def get_simple_summary(hd,bd):
    print hd
    print bd[0:9]

def get_header(hd):
    head=[]
    for i in range(len(scm_sta)):
        print i, scm_sta[i], re_srch[scm_sta[i]]
        m=re.search(re_srch[scm_sta[i]] ,hd)      
        if m:
            print i, scm_sta[i], re_srch[scm_sta[i]]
            #print m.groups()
    sys.exit()
    return head

#----------------------------
# Main
#----------------------------

def main():
  # Check Scheduler
    o_sch=check_scheduler()
    print o_sch['sch_name']
  # Check if Schema or header is available for version
    #o_scm=check_schema(o_sch['sch_name'], o_sch['sch_ver'])

    o_qst=run_command(o_sch['sch_stat'])
    if o_qst['ret'] !=0:
        print "  Error running %s" %o_sch['sch_stat']
        print "  Error         %s" %o_qst['err']
        sys.exit()
    else:
        pp.pprint( o_qst['out'][0:9])
  # Parse qstat header or xml schema
    o_hea=get_header(o_qst['out'][0].lower())
    print o_hea

  # Print simple summary
    get_simple_summary(o_hea, o_sch[1:-1])
    #running=filter(lambda f: o_hea[''] in f, o_qst['out'])
    # print status> user> queue> jobid
    

if __name__ == "__main__":
    main()


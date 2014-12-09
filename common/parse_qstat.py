#!/usr/bin/env python27

import os,sys
import subprocess as sp
import re
import pprint as pp
import copy as cp

# Some global definitions
global schedulers,sched_stat
global re_srch, re_uge_stat, re_slurm_stat, re_torque_stat
schedulers=['sge','uge', 'torque', 'slurm']
sched_stat={'sge':'qstat','uge':'qstat','torque':'qstat','slurm':'squeue'}
#sched_sche={'sge':'qstat','uge':'.xsd','torque':'','slurm':''}

sched_supp={
'uge':
{     'sch_name':'uge',
      'sch_stat':['qstat','-u','*'],
      'sch_host':['qhost','-j'],
      'sch_ver':['-help']
},
'sge':
{     'sch_name':'sge',
      'sch_stat':['qstat','-u','*'],
      'sch_host':['qhost','-j'],
      'sch_ver':['-help']
},
'slurm':
{      'sch_name':'slurm',
       'sch_stat':['squeue'],
       'sch_host':['scontrol','show','node'],
       'sch_ver':['--version']
},
'torque':
{      'sch_name':'torque',
       'sch_stat':['qstat','-a'],
       'sch_host':['pbsnodes'],
       'sch_ver':['--version']
}}

# Useful re-search compilation
#re_srch={ 'jid':'job.*?id','sta':' s|state ','que':'queue','usr':'user','slt':'slots'}
re_srch={}
re_uge_stat={ 'hd':'0','jid':'job.*?id','sta':' s|state ','que':'queue','usr':'user','slt':'slots'}
re_slurm_stat={ 'hd':'0','jid':'job.*?id','sta':' s|state ','que':'queue','usr':'user','slt':'slots'}
re_torque_stat={ 'hd':'2','jid':'job.*?id','sta':' s ','que':'queue','usr':'user[a-z]+','slt':'tsk'}

scm_sta=['sta','usr','jid','que','slt' ]
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
    global re_srch
    #
    for sch in schedulers:
      com_qst=['which',sched_stat[sch]]
      o_com=run_command(com_qst)
      if o_com['ret'] ==0:
          out=o_com['out'][0]
          obj_sch=cp.deepcopy(sched_supp[sch])
          obj_sch['env']={'PATH':out[:-len(sched_stat[sch])-1]}
          if 'uge' in out:
            obj_sch['env']['SGE_ROOT']=os.environ['SGE_ROOT']
            obj_sch['env']['SGE_CELL']=os.environ['SGE_CELL']
            #obj_sch['sch_name']='uge'
            #obj_sch['sch_stat']=['qstat','-u','*']
            #obj_sch['sch_host']=['qhost','-j']
            #obj_sch['sch_ver']=['-help']
            re_srch=cp.deepcopy(re_uge_stat)
            #print "Supports %s" %sch
          elif 'sge' in out:
            obj_sch['env']['SGE_ROOT']=os.environ['SGE_ROOT']
            obj_sch['env']['SGE_CELL']=os.environ['SGE_CELL']
            #obj_sch['sch_name']='sge'
            #obj_sch['sch_stat']=['qstat','-u','*']
            #obj_sch['sch_host']=['qhost','-j']
            #obj_sch['sch_ver']=['-help']
            re_srch=cp.deepcopy(re_uge_stat)
          elif 'torque' in out:
            obj_sch['env']['PBS_HOME']=''
            obj_sch['env']['PBS_SERVER']=''
            #obj_sch['sch_name']='torque'
            #obj_sch['sch_stat']=['qstat','-a']
            #obj_sch['sch_host']=['pbsnodes']
            #obj_sch['sch_ver']=['--version']
            re_srch=cp.deepcopy(re_torque_stat)
            #print "Supports %s" %sch
          elif 'slurm' in out:
            #obj_sch['env']['SLURM_ROOT']=os.environ['SLURM_ROOT']
            #obj_sch['sch_name']='slurm'
            #obj_sch['sch_stat']=['squeue']
            #obj_sch['sch_host']=['scontrol','show','node']
            #obj_sch['sch_name']='slurm'
            #obj_sch['sch_ver']=['--version']
            re_srch=cp.deepcopy(re_slurm_stat)
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
    print re_srch
    return obj_sch

def get_elements_byschema(xml_doc, xml_sche, xml_typ):
    print 'testing'
    nam_spc = xml_doc.xpath("//xsd:element[@type = $n]/@name",
                            namespaces={"xsd": 
                                        "http://www.w3.org/2001/XMLSchema"},
                            n=xml_typ)

def check_schema(sch,ver):
    ava_scm={'uge-8.1.7':''}


def get_header(hd):
    #global re_srch
    head={}
    for i in range(len(scm_sta)):
        #head.append(None)
        #print 'Searching',i, scm_sta[i], re_srch[scm_sta[i]]
        m=re.search(re_srch[scm_sta[i]] ,hd,re.IGNORECASE)      
        if m:
            print 'Found ',i, scm_sta[i], re_srch[scm_sta[i]], hd[m.span()[0]:m.span()[1]]
            head[scm_sta[i]]=m.span()
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
    o_qst['out']=filter(lambda x: not re.match(r'^\s*$', x), o_qst['out'])
    pp.pprint(o_qst['out'][2])
    if o_qst['ret'] !=0:
        print "  Error running %s" %o_sch['sch_stat']
        print "  Error         %s" %o_qst['err']
    else:
        pp.pprint( o_qst['out'][0:9])
  # Parse qstat header or xml schema
    hd=int(re_srch['hd'])
    o_hea=get_header(o_qst['out'][hd].lower())
    #print 'Head',o_qst['out'][hd]
    #print 'Head',o_hea
  # Print simple summary
    usr_jbs={}
    for line in o_qst['out'][hd:]:
        u=line[o_hea['usr'][0]:].split()[0];
        j=line[o_hea['jid'][0]:].split()[0];
        q=line[o_hea['que'][0]:].split()[0];
        l=line[o_hea['slt'][0]:].split()[0];
        if u in usr_jbs:
            usr_jbs[u]+=cp.deepcopy([(j,l)])
        elif u not in usr_jbs and '----' not in u:
            usr_jbs[u]=cp.deepcopy([(j,l)])
    #pp.pprint(usr_jbs)
    prn_len=3
    for u in usr_jbs:
        j=usr_jbs[u]
        uset=list(set(j)); lset=len(j)
        #
        TSlts=sum([int(x[1]) for x in j if re.match(r'[0-9]+', x[1]) ] )
        #
        if lset>prn_len:
            print " %10s %10s %10s %s..."  %(u,TSlts, lset, uset[0:min(prn_len,lset)] )
        else:
            print " %10s %10s %10s %s"      %(u,TSlts, lset, uset[0:lset])
    

if __name__ == "__main__":
    main()


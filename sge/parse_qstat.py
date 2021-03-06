#!/usr/bin/env python27

import os,sys,re
import copy as cp
import pprint as pp
import subprocess as sp

# Some global definitions

def define_global():
  # Global definitions
    global sched_re, sched_supp, scm_sta
  # Supported schedulers
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
  # Userful re searches
    sched_re={
    'uge':   {'hd':'0','jid':'job.*?id','sta':' s|state ','que':'queue',   'usr':'user','slt':'slots'},
    'sge':   {'hd':'0','jid':'job.*?id','sta':' s|state ','que':'queue',   'usr':'user','slt':'slots'},
    'slurm': {'hd':'0','jid':'job.*?id','sta':' st ',     'que':'partition','usr':'user','slt':'nodes'},
    'torque':{'hd':'2','jid':'job.*?id','sta':' s ',      'que':'queue'    ,'usr':'user[a-z]+','slt':'tsk'},
    }
  # Schema/order for desired output status>user>jid
    scm_sta=['sta','usr','jid','que','slt' ]
    scm_que=['que','usr','jid']

def run_command(com_inp):
    com_out={}
    try:
        p=sp.Popen(com_inp,stdout=sp.PIPE, stderr=sp.PIPE)
    except:
        print "    %s Command failed" %com_inp
    # some issues on carver python26 with p.wait
    #ret=p.wait()
    #if p:
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
    for sch in sched_supp.keys():
      com_qst=['which',sched_supp[sch]['sch_host'][0]]
      o_com=run_command(com_qst)
      if o_com['ret'] ==0:
          out=o_com['out'][0]
          obj_sch=cp.deepcopy(sched_supp[sch])
          rkey='re_'+sch+'_stat'
          re_srch=cp.deepcopy(sched_re[sch])
          obj_sch['env']={'PATH':out[:-len(sched_supp[sch]['sch_host'])-1]}
          if 'uge' in out:
            obj_sch['env']['SGE_ROOT']=os.environ['SGE_ROOT']
            obj_sch['env']['SGE_CELL']=os.environ['SGE_CELL']
            #print "Supports %s" %sch
          elif 'sge' in out:
            obj_sch['env']['SGE_ROOT']=os.environ['SGE_ROOT']
            obj_sch['env']['SGE_CELL']=os.environ['SGE_CELL']
            #re_srch=cp.deepcopy(re_sge_stat)
          elif 'torque' in out:
            obj_sch['env']['PBS_HOME']=''
            obj_sch['env']['PBS_SERVER']=''
            #print "Supports %s" %sch
          elif 'slurm' in out:
            #obj_sch['env']['SLURM_ROOT']=os.environ['SLURM_ROOT']
            #print re_slurm_stat
            print "Supports %s" %sch
          else:
            print "Found no support for %s" %sch
            #sys.exit()
          com_ver=[obj_sch['sch_stat'][0]]+obj_sch['sch_ver']
          obj_sch['sch_ver']=get_version(com_ver)
      else:
        print "Finding scheduler %s ... Failed" %sch
        #sys.exit()
    pp.pprint(obj_sch)
    if 'sch_stat' in obj_sch:
        print '''
        Checking scheduler support %s
        Command tried              %s
        Found support for          (%s, %s)
        ''' %(sched_supp.keys(), obj_sch['sch_stat'],obj_sch['sch_name'],obj_sch['sch_ver'])
    print re_srch
    #sys.exit()
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
  # Define global variabes
    define_global()
  # Check Scheduler
    o_sch=check_scheduler()
  # Check if Schema or header is available for version
    #o_scm=check_schema(o_sch['sch_name'], o_sch['sch_ver'])
  # Run qstat
    o_qst=run_command(o_sch['sch_stat'])
    o_qst['out']=filter(lambda x: not re.match(r'^\s*$', x), o_qst['out'])
    pp.pprint(o_qst['out'][2])
    if o_qst['ret'] !=0:
        print "  Error running %s" %o_sch['sch_stat']
        print "  Error         %s" %o_qst['err']
    else:
        pp.pprint( o_qst['out'][0:9])
  # Parse qstat header or xml schema
    print re_srch['hd']
    print 'Hd',re_srch['hd']
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


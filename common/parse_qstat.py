#!/usr/bin/env python27

import os,sys,re
import copy as cp
import pprint as pp
import subprocess as sp
from string import digits

# Some global definitions

def define_global():
  # Global definitions
    global sched_re, sched_supp, sched_stat_ou, scm_sta
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
    'uge':   {'hd':'0','adj':'l','jid':'job.*?id','sta':' s|state ','que':'queue',   'usr':'user','slt':'slots','sub':'submit/start at'},
    'sge':   {'hd':'0','adj':'l','jid':'job.*?id','sta':' s|state ','que':'queue',   'usr':'user','slt':'slots'},
    'slurm': {'hd':'0','adj':'r','jid':'job.*?id','sta':' st ',     'que':'partition','usr':'user','slt':'nodes'},
    'torque':{'hd':'2','adj':'l','jid':'job.*?id','sta':' s ',      'que':'queue'    ,'usr':'user[a-z]+','slt':'tsk'},
    }

    sched_stat_ou={
    'uge': {'jid':'[0-9]+','sta':'r|qw','que':'([\S]+@[a-zA-Z0-9-]+)','usr':'[a-zA-Z0-9-]+','slt':'[0-9]+','sub':'([0-9//]+)\s([0-9:]+)'}, 
    'sge': {'jid':'[0-9]+','sta':'r|qw','que':'([\S]+@[a-zA-Z0-9-]+)','usr':'[a-zA-Z0-9-]+','slt':'[0-9]+','sub':'([0-9//]+)\s([0-9:]+)'},
    'slurm':  [],
    'torque':{'jid':'[0-9]+','sta':'r|q','que':'([a-zA-Z0-9-_.]+)','usr':'[a-zA-Z0-9-]+','slt':'[0-9]+','sub':'([0-9//]+)\s([0-9:]+)'}
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
            print "Finding scheduler %8s ... Passed" %sch
            #print "Supports %s" %sch
          elif 'sge' in out:
            obj_sch['env']['SGE_ROOT']=os.environ['SGE_ROOT']
            obj_sch['env']['SGE_CELL']=os.environ['SGE_CELL']
            print "Finding scheduler %8s ... Passed" %sch
            #re_srch=cp.deepcopy(re_sge_stat)
          elif 'torque' in out:
            obj_sch['env']['PBS_HOME']=''
            obj_sch['env']['PBS_SERVER']=''
            #print "Supports %s" %sch
            print "Finding scheduler %8s ... Passed" %sch
          elif 'slurm' in out:
            #obj_sch['env']['SLURM_ROOT']=os.environ['SLURM_ROOT']
            print "Finding scheduler %8s ... Passed" %sch
          else:
            print "Found no support for %s" %sch
            #sys.exit()
          com_ver=[obj_sch['sch_stat'][0]]+obj_sch['sch_ver']
          obj_sch['sch_ver']=get_version(com_ver)
      else:
        print "Finding scheduler %s ... Failed" %sch
    #pp.pprint(obj_sch)
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

def get_hd_line(out,exp):
  # Find header in out.split() based in exp
    head=None
    for n in range(min(99,len(out))):
        l=out[n]
        #print n,l, exp
        m1=re.search(exp['jid'], l, re.IGNORECASE)
        m2=re.search(exp['que'], l, re.IGNORECASE)
        m3=re.search(exp['usr'], l, re.IGNORECASE)
        if m1 and m2 and m3:
           head=n
           break
    #print head
    #sys.exit()
    return head


def get_header(hd):
  # Get span of header variables
    head={}
    for i in range(len(scm_sta)):
        m=re.search(re_srch[scm_sta[i]] ,hd,re.IGNORECASE)      
        if m:
            #print 'Found ',i, scm_sta[i], re_srch[scm_sta[i]], hd[m.span()[0]:m.span()[1]]
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
  # Run qstat
    o_qst=run_command(o_sch['sch_stat'])
    if o_qst['ret'] !=0:
        print "  Error running %s" %o_sch['sch_stat']
        print "  Error         %s" %o_qst['err']
  # Remove empty lines and hyphen-only lines
    o_qst['out']=filter(lambda x: not re.match(r'^\s*$',  x), o_qst['out'])
    o_qst['out']=filter(lambda x: not re.match(r'[- ]+$', x), o_qst['out'])
  # Print some
    prn_len=5
    pp.pprint( o_qst['out'][0: min(prn_len,len(o_qst['out']))] )
    print '...'
    pp.pprint( o_qst['out'][ -min(prn_len,len(o_qst['out'])) :-1] )
    #sys.exit()
  # Set header line number in truncated output
    hline=get_hd_line(o_qst['out'], sched_re[o_sch['sch_name']] )
    if hline==None:
        hd=int(re_srch['hd'])
    else :
        hd=hline
  # Get header variables
    #sys.exit()
    o_hea=get_header(o_qst['out'][hd].lower())
    print o_hea
    #sys.exit()
  # Create simple representation of user jobs with user keys
    usr_jbs={}
    sts_jbs={}
    que_jbs={}
    nod_jbs={}
    for line in o_qst['out'][hd:]:
        u=line[o_hea['usr'][0]:].split()[0];
        j=line[o_hea['jid'][0]:].split()[0];
        #q=line[o_hea['que'][0]:].split()[0];       
        #q=re.search(sched_stat_ou[o_sch['sch_name']]['que'],line)
        s=line[o_hea['sta'][0]:].split()[0];
        l=line[o_hea['slt'][0]:].split()[0];
        q=line[o_hea['que'][0]:].split()[0];
        if 'ge' in o_sch['sch_name']:
          q=re.search(sched_stat_ou[o_sch['sch_name']]['que'],line)
          if q:
            qi=q.group().split('@')[0]
            ni=q.group().split('@')[1].translate(None,digits)
          else:
            qi=q
            ni=None
        # User
        if u in usr_jbs:
            usr_jbs[u]+=cp.deepcopy([(j,l)])
        elif u not in usr_jbs and '----' not in u:
            usr_jbs[u]=cp.deepcopy([(j,l)])
        # Status
        if s in sts_jbs:
            sts_jbs[s]+=cp.deepcopy([(j,l)])
        elif s not in sts_jbs and '----' not in s and 'state' not in s:
            sts_jbs[s]=cp.deepcopy([(j,l)])
        # Queue
        #if q:
        #    print q
            #qi=q.group().split('@')[0]
            #ni=q.group().split('@')[1].translate(None,digits)
        if qi in que_jbs:
            que_jbs[qi]+=cp.deepcopy([(j,l)])
        elif qi not in que_jbs and '----' not in qi:
            que_jbs[qi]=cp.deepcopy([(j,l)])
        if ni in nod_jbs:
                nod_jbs[ni]+=cp.deepcopy([(j,l)])
        elif ni and ni not in nod_jbs and '----' not in ni:
                nod_jbs[ni]=cp.deepcopy([(j,l)])



    #pp.pprint(usr_jbs)
    prn_len=3
    print '''
    /* By User Jobs Slots */'''
    for u in usr_jbs:
        j=usr_jbs[u]
        uset=list(set(j)); lset=len(j)
        #
        TSlts=sum([int(x[1]) for x in j if re.match(r'[0-9]+', x[1]) ] )
        #
        if lset>prn_len:
            print " %10s %10s %10s %s..."   %(u,lset,TSlts, uset[0:min(prn_len,lset)] )
        else:
            print " %10s %10s %10s %s"      %(u,lset,TSlts, uset[0:lset])

    print '''
/* By %10s %16s %16s */''' %('Status', 'Jobs','Slots')
    for s in sts_jbs:
        j=sts_jbs[s]
        sset=list(set(j)); lset=len(j)
        #
        TSlts=sum([int(x[1]) for x in j if re.match(r'[0-9]+', x[1]) ] )
        print " %16s %16s %16s"      %(s,lset,TSlts)
        #
        #if lset>prn_len:
        #    print " %10s %10s %10s %s..."   %(s,TSlts, lset, sset[0:min(prn_len,lset)] )
        #else:
        #    print " %10s %10s %10s %s"      %(s,TSlts, lset, sset[0:lset])

    prn_len=2
    print '''
/* By %10s %16s %16s */''' %('Queue', 'Jobs','Slots')
    for q in que_jbs:
        j=que_jbs[q]
        qset=list(set(j)); lset=len(j)
        #
        TSlts=sum([int(x[1]) for x in j if re.match(r'[0-9]+', x[1]) ] )
        print " %16s %16s %16s"      %(q,lset,TSlts)
        #
        #if lset>prn_len:
        #    print " %10s %10s %10s %s..."   %(q,TSlts, lset, qset[0:min(prn_len,lset)] )
        #else:
        #    print " %10s %10s %10s %s"      %(q,TSlts, lset, qset[0:lset])

    print '''
/* By %10s %16s %16s */''' %('Hostgrps', 'Jobs','Slots')
    for n in nod_jbs:
        j=nod_jbs[n]
        qset=list(set(j)); lset=len(j)
        TSlts=sum([int(x[1]) for x in j if re.match(r'[0-9]+', x[1]) ] )
        print " %16s %16s %16s"      %(n,lset,TSlts)
        #TSlts=sum([int(x[1]) for x in j if re.match(r'[0-9]+', x[1]) ] )
        #
        #if lset>prn_len:
        #    print " %10s %10s %10s %s..."   %(n,TSlts, lset, qset[0:min(prn_len,lset)] )
        #else:
        #    print " %10s %10s %10s %s"      %(n,TSlts, lset, qset[0:lset])

if __name__ == "__main__":
    main()


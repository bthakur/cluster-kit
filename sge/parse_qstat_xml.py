#!/usr/bin/env python27

import os,sys,re
import copy as cp
import pprint as pp
import subprocess as sp

from xml.dom import minidom
import xml.etree.ElementTree as ET


# Some global definitions

def define_global():
  # Global definitions
  # formats
    global format_T
    format_T='{:<30}{:<10}{:<10}{:<10}'
  # Supported schedulers
    global sched_supp
    sched_supp={
    'uge':
    {     'sch_name':'uge',
          'sch_stat':['qstat','-u','*','-xml'],
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
           'sch_stat':['qstat','-xml'],
           'sch_host':['pbsnodes'],
           'sch_ver':['--version']
    }}
  # Supported schedulers
    site_supp={
    'genepool':
    {     'env_dir_sge_root':'/opt/uge/genepool/uge/',
          'env_dir_sge_cell':'genepool',
    },
    'slurm':
    {     'env_dir_slurm_top':'/opt/slurm',
          'env_dir_slurm_cell':'genepool',
    }}

def etree_to_dict(t):
    d = {t.tag : map(etree_to_dict, t.iterchildren())}
    d.update(('@' + k, v) for k, v in t.attrib.iteritems())
    d['text'] = t.text
    return d

def minidom_to_dict(t):
    return t

def run_command(com_inp):
    com_out={}
    com_out['out']=None
    p=None
    try:
        p=sp.Popen(com_inp,stdout=sp.PIPE, stderr=sp.PIPE)
    except:
        print "    %s Command failed" %com_inp
	#sys.exit()
    # some issues on carver python26 with p.wait
    #ret=p.wait()
    com_out['out']=None
    if p:
       out,err=p.communicate()
       com_out['ret']=p.returncode
       com_out['inp']=com_inp
       com_out['err']=err
    #if p.returncode ==0 :
    #    com_out['out']=str.split(out,'\n')
       com_out['out']=out
    return com_out


def get_elements_byschema(xml_doc, xml_sche, xml_typ):
    print 'testing'
    nam_spc = xml_doc.xpath("//xsd:element[@type = $n]/@name",
                            namespaces={"xsd": 
                                        "http://www.w3.org/2001/XMLSchema"},
                            n=xml_typ)


#----------------------------
# Main
#----------------------------

def main():
  # Define global variabes
    define_global()
  # Check Scheduler
    #o_sch=check_scheduler()
  # Check if Schema or header is available for version
    #o_scm=check_schema(o_sch['sch_name'], o_sch['sch_ver'])

  # Run qstat or read from a file
    sch_stat=sched_supp['uge']['sch_stat']
    o_qst=run_command(sch_stat)
    # Using etree
    if True:
       if o_qst['out'] != None:
          xmlout=o_qst['out']
          root = ET.fromstring(xmlout)
       else:
          xmlout=ET.parse('qstat.out')
          root = xmlout.getroot()
       #
       schema = ET.parse('qstat.xsd')

    # Using minidom
    if False:
       if o_qst['out'] != None:
          xmlout=o_qst['out']
          root = minidom.parseString(xmlout)
       else:
          root = minidom.parse('qstat.out')
       #
       schema = minidom.parse('qstat.xsd')

  #
    jobs_by_users={}

  # Using minidom
    if False: 
       jobs = root.getElementsByTagName("job_list")
       for job in jobs:
	   print job.tagName
	   for elem in job.childNodes:
	       #if elem.nodeName != '#text':
	       if elem.nodeType != elem.TEXT_NODE:
	          print elem.nodeName
	          print elem.toxml()
	          for e in elem.childNodes:
		      print '|---',e.nodeName,  e.nodeValue
	       #sys.exit()
		
	      #print elem.getElementsByTagName(elem.nodeName)
	   #    node_jid=elem.nodeName
           sys.exit()

  # Using etree
    if True: 
        running=0
        allrunning=[]
        for job in root.findall(".//*[@state='running']"):
           #print ET.tostring(job)
	   running+=1
	   jrunning={}
           for e in job:
               #print ET.tostring(e)
               #print   e.tag, e.text
	       jrunning[e.tag]=e.text
               #jobs[e.tab]=e.text
	   #print jrunning
	   allrunning.append(cp.deepcopy(jrunning))
       #
       #print 'Running jobs',running
       #
        pending=0
        allpending=[]
        for job in root.findall(".//*[@state='pending']"):
           #print ET.tostring(job)
           pending+=1
	   jpending={}
           for e in job:
                #print ET.tostring(e)
                #print   e.tag, e.text
		jpending[e.tag]=e.text
	   #print jpending.values()
	   allpending.append(cp.deepcopy(jpending))
    #
        print 'Running jobs',running
        #print pp.pprint(allrunning)
        print 'Pending jobs',pending
        #print pp.pprint(allpending)

  # Analytics on allrunning
	jobs_by_user={}
	jobs_by_node={}
	jobs_by_queue={}
	#
	jobs_by_all={}
	jobs_by_all['AllUsers']=[0,0,0,set()]
	jobs_by_all['AllQueues']=[0,0,0,set()]
        jobs_by_all['AllNodes']=[0,0,0,set()]
	print "Jobs_by_user Jobs Tasks Slots JobID's"
	for j in allrunning:
            job_by_user={}
	    qname=j['queue_name']
	    jobowner=j['JB_owner']
	    jobnumber=j['JB_job_number']
	    jobstart=j['JAT_start_time']
	    jobslots=j['slots']
	#   queue processing
	    qname_q=qname.split('@')[0]
	    qname_r=qname.split('@')[1][0:4]
            #print qname_q, qname_r
	    jobs_by_all['AllUsers'][1]+=int(1)
	    jobs_by_all['AllUsers'][2]+=int(jobslots)
            jobs_by_all['AllQueues'][1]+=int(1)
            jobs_by_all['AllQueues'][2]+=int(jobslots)
            jobs_by_all['AllNodes'][1]+=int(1)
            jobs_by_all['AllNodes'][2]+=int(jobslots)
	    jobs_by_all['AllUsers'][3].add(jobnumber)
            jobs_by_all['AllQueues'][3].add(jobnumber)
            jobs_by_all['AllNodes'][3].add(jobnumber)
	    #
	    if jobowner in jobs_by_user:
		jobs_by_user[jobowner][1]+=int(1)
		jobs_by_user[jobowner][2]+=int(jobslots)
		jobs_by_user[jobowner][3].add(jobnumber)
		#jobs_by_user[jobowner]+=[jobslots,qname]
	    else:
		jobs_by_user[jobowner]=[1,int(1),int(jobslots),set([jobnumber])]
	#
	    if qname_q in jobs_by_queue:
                jobs_by_queue[qname_q][1]+=int(1)
                jobs_by_queue[qname_q][2]+=int(jobslots)
                jobs_by_queue[qname_q][3].add(jobnumber)
                #jobs_by_user[jobowner]+=[jobslots,qname]
            else:
                jobs_by_queue[qname_q]=[1,int(1),int(jobslots),set([jobnumber])]
	#
            if qname_r in jobs_by_node:
                jobs_by_node[qname_r][1]+=int(1)
                jobs_by_node[qname_r][2]+=int(jobslots)
                jobs_by_node[qname_r][3].add(jobnumber)
                #jobs_by_user[jobowner]+=[jobslots,qname]
            else:
                jobs_by_node[qname_r]=[1,int(1),int(jobslots),set([jobnumber])]
	#
	for v0 in ['user', 'queue', 'node']:
	    v1='jobs_by_'+v0
	    d=locals()[v1]
	    print '---------'
	    sumj=0
	    print( format_T.format(' ','Jobs','Tasks', 'Slots' ))
	    for j,l in d.items():
		 print( format_T.format(j,len(l[3]),l[1], l[2] ))
	    print '----------'
	    print( format_T.format('ALL-'+v0,len(l[3]),l[1], l[2] ))	

	print '-------'
	#
	
        #print 'Running jobs',running
        #print pp.pprint(allrunning)
        #print 'Pending jobs',pending
	
	sys.exit()

  # Analytics on allpending
        jobs_by_user={}
        jobs_by_all={}
        jobs_by_all['AllUsers']=[0,0,0,set()]
        print "Jobs_by_user Jobs Tasks Slots JobID's"
        for j in allpending:
            job_by_user={}
            qname=j['queue_name']
            jobowner=j['JB_owner']
            jobnumber=j['JB_job_number']
            jobstart=j['JB_submission_time']
            jobslots=j['slots']
            jobs_by_all['AllUsers'][1]+=int(1)
            jobs_by_all['AllUsers'][2]+=int(jobslots)
            #jobs_by_all['AllUsers'][3].add(jobnumber)
            if jobowner in jobs_by_user:
                jobs_by_user[jobowner][1]+=int(1)
                jobs_by_user[jobowner][2]+=int(jobslots)
                jobs_by_user[jobowner][3].add(jobnumber)
                #jobs_by_user[jobowner]+=[jobslots,qname]
            else:
                jobs_by_user[jobowner]=[1,int(1),int(jobslots),set([jobnumber])]
        #

        # Sort and get unique jobids
        #jobs_by_all['AllUsers'][0]=0
        for j,l in jobs_by_user.items():
            # put the set back as a list
            jobs_by_user[j][3]=list(l[3])
            jobs_by_user[j][0]=len(jobs_by_user[j][3])
            jobs_by_all['AllUsers'][0]+=jobs_by_user[j][0]
        # Now for all users
        jobs_by_all['AllUsers'][3]=list(l[3])
        pp.pprint( jobs_by_user,depth=2,indent=4 )
        print '    ----------'

        pp.pprint( jobs_by_all,depth=2,indent=4 )
        print '          '

if __name__ == "__main__":
     main()

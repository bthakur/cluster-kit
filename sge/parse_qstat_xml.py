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
  # Supported schedulers
    global sched_supp
    sched_supp={
    'uge':
    {     'sch_name':'uge',
          'sch_stat':['qstat','-u','b*','-xml'],
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

def check_schema(sch,ver):
    ava_scm={'uge-8.1.7':''}

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
	   #print job.data
	   #print job.getElementsByTagName('JB_owner')
	   #print job.getElementsByTagName('JB_owner').toxml()
	   #print job.getElementsByTagName('JB_job_number')
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
       for job in root.findall(".//*[@state='running']"):
            print 'Tag',job.tag
            print 'Value', job.text
            print ET.tostring(job)
            #print job.attrib.get('JB_owner');
            #print job.attrib.get('JB_job_number')
            #print list(job)
            for e in job:
                #print  e.text
                #print e.attrib.get('JB_owner')
                #sys.exit()
                print ET.tostring(e)
                #print e.tab, e.text
                #jobs[e.tab]=e.text
    #
    sys.exit()

   # All running jobs
    #for jobs in root:
    #	print 'Running Jobs'
#    for job in root.findall(".//*[@state='running']"):
#
    

    sys.exit()
		
    #pp.pprint(jobs)
    sys.exit()
    for job in root.findall(".//*[@state='running']"):
	    print 'Tag',job.tag
	    print 'Value', job.text
	    #sys.exit()
	    #print ET.tostring(job)
	    #print job.attrib.get('JB_owner');
	    #print job.attrib.get('JB_job_number')
	    #print list(job)
	    #for e in job:
		#print  e.text
                #print e.attrib.get('JB_owner')
                #sys.exit()
		#print ET.tostring(e)
		#print e.tab, e.text
		#jobs[e.tab]=e.text
    print 'Pending Jobs'
    sys.exit()
    for job in root.findall(".//*[@state='pending']"):
            #print job.tag, job.attrib
            print job
            #print job.attrib
    #print 'pending'
    #for jobs in root.findall(".//*[@state='pending']"):
    #    for job in jobs:
    #        print job

    # Jobs requesting 16 slots
    #for job in root.findall(".//job_list[@state='running']/[slots='16']"):
    #	print job

    #for job in root.findall(".//job_list[@state='pending']/"):
    #    print '   |--',job.tag, job.attrib, job.text


if __name__ == "__main__":
     main()


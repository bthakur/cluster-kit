#!/usr/bin/env python27

import os,sys,re
import copy as cp
import pprint as pp
import subprocess as sp
#from xml.dom.minidom import pars
import xml.etree as et
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

def run_command(com_inp):
    com_out={}
    try:
        p=sp.Popen(com_inp,stdout=sp.PIPE, stderr=sp.PIPE)
    except:
        print "    %s Command failed" %com_inp
	sys.exit()
    # some issues on carver python26 with p.wait
    #ret=p.wait()
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
  # Run qstat
    sch_stat=sched_supp['uge']['sch_stat']
    o_qst=run_command(sch_stat)
    xmlout=o_qst['out']
    #dom2 = parseString( out )
    #print dom2.toxml()
    #o_qst['out']=filter(lambda x: not re.match(r'^\s*$', x), o_qst['out'])
    #xmlschema_doc = etree.parse('qstat.xsd')
    #xml_doc = etree.parse(xmlout)
    #schema = et.parse("qstat.xsd")
    schema = ET.parse('qstat.xsd')
    #tree = ET.ElementTree(file='qstat.xsd')
    root = ET.fromstring(xmlout)

    print root.tag
    print root.attrib
    for child in root:
        print child.tag, child.attrib
	
if __name__ == "__main__":
    main()


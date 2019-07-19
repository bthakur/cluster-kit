#!/usr/bin/env python

import csv
import pprint as pp
import argparse
import sys,os
from copy import deepcopy as dp

parser = argparse.ArgumentParser()

parser.add_argument('-f', action='store',
                     dest='input_file',
                     nargs=1, help="Accounting file to be parsed")

args = parser.parse_args()
if not args.input_file:
   parser.print_help()
   sys.exit(0)

global jobs_by_users
global jobs_by_queues


jobs_by_user={}
jobs_by_queue={}
jobs_by_proj={}
jobs_by_wall={}
jobs_by_vmem={}
jobs_by_user['Alluser']=dp([int(0),int(0),int(0),int(0)])
jobs_by_queue['Allqueue']=[int(0),int(0),int(0),int(0)]

with open(args.input_file[0], 'rb') as f:
#with open('test.100', 'rb') as f:
     for row in csv.reader(f, delimiter=' ', skipinitialspace=True):
         #print '|'.join(row)
         #print len(row)
         #pp.pprint(row)
         user=row[11]
         jobid=row[3]
         queue=row[12]
         slots=row[6]
         memory=row[-16]
         req_mem=row[13]
         cluster=row[23]
         walltime=row[-5]
         tsub=row[7]
         tbeg=row[10]
         tend=row[2]
         twait=int(tbeg)-int(tsub)
         trun=int(tend)-int(tbeg)
         #print len(row),user, jobid,queue, cluster, slots, walltime,trun,twait,memory,req_mem
         job_success=trun > 5
         if job_success:
           #
           for key in ['user', 'queue']:
            #By User
            Allkey=str('All'+str(key))
            Dname=str('jobs_by_'+str(key))
            #print type(globals())
            jobs_by=globals()[Dname]
            jobs_by[Allkey][0]+=int(1)
            jobs_by[Allkey][1]+=int(slots)
            jobs_by[Allkey][2]+=int(walltime)
            jobs_by[Allkey][3]+=int(memory)
            if user in jobs_by:
               jobs_by[key][0]+=int(1)
               jobs_by[key][1]+=int(slots)
               jobs_by[key][2]+=int(walltime)
               jobs_by[key][3]+=int(memory)
               #jobs_by[key]+=[slots,walltime,trun,memory]
               pp.pprint(jobs_by)
            else:
               jobs_by[key]=[int(slots),int(walltime),int(trun),int(memory)]

#By Usr
print pp.pprint(jobs_by_user)




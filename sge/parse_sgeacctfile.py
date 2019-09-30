#!/usr/bin/env python

#Bhupender Thakur 2019

import argparse as ap
import datetime as dt
import sys

def epoch_to_date(secs_i):
    t_date=dt.datetime.fromtimestamp(
           secs_i.strftime('%Y-%m-%d:%H%M'))
    return t_date

parser = ap.ArgumentParser()

parser.add_argument('-f',action='store',dest='file_inp',nargs=1,
                help="Input accounting file to be parsed")

args = parser.parse_args()

if args.file_inp:
    inputf = args.file_inp[0]
    with open(inputf,'rb') as fi:
        lines=fi.readlines()
else:
    parser.print_help()
    sys.exit()

OneK=1000.
OneM=1000000.

#print dt.datetime.tzinfo.est()
t_now=dt.datetime.today()
t_epoch=dt.datetime(1970,1,1)
t_beg2019=dt.datetime(2019,01,01,0,0)
#
t_nowsecs=t_now
t_del2019secs=(t_beg2019 - t_epoch).total_seconds()
t_del2019days=(t_beg2019 - t_epoch).days
print t_epoch, t_beg2019,t_now
print t_del2019secs,t_del2019days

#sys.exit()

for l in lines:
    line=l.split(':')
    if l[0] != '#':
        queue=line[0]
        host=line[1]
        user=line[3]
        jobid=line[5]
        #slots=
        #vmem
        tsub=float(line[8])/OneK;  tsub_19=tsub-t_del2019secs
        tbeg=float(line[9])/OneK;  tbeg_19=(tbeg-t_del2019secs)
        tend=float(line[10])/OneK; tend_19=(tend-t_del2019secs)
        twai=round(tbeg_19-tsub_19,2)
        trun=round(tend_19-tbeg_19,2)
        #print l
        #print queue,host,user,jobid,tsub_19,tbeg_19,tend_19
        print queue,host,user,jobid,twai,trun



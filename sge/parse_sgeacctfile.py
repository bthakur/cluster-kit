#!/usr/bin/env python

#Bhupender Thakur 2019

import argparse as ap
import sys

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
for l in lines:
    line=l.split(':')
    if l[0] != '#':
        queue=line[0]
        host=line[1]
        user=line[3]
        jobid=line[5]
        tsub=int(line[8]/OneM); tbeg=int(line[9]/OneM); tend=int(line[10]/OneM)
        #print l
        print queue,host,user,jobid,tsub,tbeg,tend




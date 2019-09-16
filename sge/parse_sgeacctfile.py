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

for l in lines:
    #print line.split(':')
    line=l.split(':')
    if l[0] != '#':
        queue=line[0]
        host=line[1]
        user=line[3]
        jobid=line[5]
        tsub=line[8]
        tbeg=line[9]
        tend=line[10]
        print l
        print queue,host,user,jobid,tsub,tbeg,tend




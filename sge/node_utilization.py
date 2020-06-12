#!/usr/bin/env python3

# Bhupender Thakur 2019

import argparse as ap
import datetime as dt
import pprint as pp
import numpy as np
import math
import sys
import re
import traceback
from collections import OrderedDict as od
from collections import defaultdict


def date_to_year(date_i):
    delta = {}
    delta_year_start = date_i - dt.datetime(date_i.year, 1, 1)
    delta['day'] = delta_year_start.days+1
    delta['sec'] = delta_year_start.total_seconds()
    return delta


def epoch_to_year(secs_i):
    delta = {}
    curr_year = dt.datetime.now().year
    date_i = dt.datetime.fromtimestamp(secs_i)
    #
    date_year_start = dt.datetime(curr_year, 1, 1)
    delta_year_start = date_i - date_year_start
    delta['sec'] = delta_year_start.total_seconds()
    delta['day'] = delta_year_start.days+1
    return delta


def parse():
    parser_i = ap.ArgumentParser()
    parser_i.add_argument('-f', action='store', dest='file_inp', nargs=1,
                          help="Input accounting file to be parsed")
    return parser_i


parser = parse()
args = parser.parse_args()

if args.file_inp:
    inputf = args.file_inp[0]
    with open(inputf, 'rb') as fi:
        lines = fi.readlines()
else:
    parser.print_help()
    sys.exit()


OneK = 1000.
OneM = 1000000.

minDay = 365
maxDay = 0
minHour = 10000
maxHour = 0

days = od()
nodes = od()
seconds = od()
hours = od()
#hours = defaultdict(list)

re_pattern = "h_vmem=([\d]+)(\w)"
c_pattern = re.compile(re_pattern)

for l in enumerate(lines):
    # print(type(l))
    line = l[1].decode("utf-8", errors="ignore").split(':')
    # print(l)
    if not line[0].startswith('#'):
        queue = line[0]
        host = line[1].split('.')[0]
        user = line[3]
        jobid = line[5]
        # maxvmem,maxrss,maxpss = 
        # cpucycles = line[36]
        # intmem = line[37]
        # io = line[38]
        hres = line[39].strip()
        # slots=
        # vmem
        proj = line[31]
        pe = line[33]
        slots = int(line[34])

        # Epoch start times to secs from millisecs
        tesub = float(line[8])/OneK
        tebeg = float(line[9])/OneK
        teend = float(line[10])/OneK

        # Yearly times since start of the year
        tsub_this_year = epoch_to_year(tesub)['sec']
        tbeg_this_year = epoch_to_year(tebeg)['sec']
        tend_this_year = epoch_to_year(teend)['sec']
            
        # day = tbeg_this_year['day']
        # sec = tbeg_this_year['sec']

        failed = line[11]

        if tebeg == 0 and tend_this_year > 0:
            print("error", jobid, queue, host, user, proj, failed)

        else:
        
            # Get requested slots
            match = c_pattern.search(hres)
            if match:
                # print("matching", match.group(), match.start(), match.end())
                # print("matching", match[1], match[2])
                if match[2].lower() == 'g':
                    mem = float(slots)*float(match[1])
                elif match[2].lower() == 'm':
                    mem = (float(slots)*float(match[1]))/1000.
                else:
                    mem = 0.0
                # print("matching", hres[match.start(): match.end()])
                    


            tbeg = float( tbeg_this_year )/3600.
            tend = float( tend_this_year )/3600.
            trun = tend - tbeg

            tbeg_hour = math.floor( tbeg )
            tend_hour = math.floor( tend )

            tbeg_day = math.floor( tbeg_hour/( 24. ))
            tend_day = math.floor( tend_hour/( 24. ))

            maxDay = max(tend_day, maxDay)
            minDay = min(tbeg_day, minDay)

            maxHour = max(tend_hour, maxHour)
            minHour = min(tbeg_hour, minHour)

            # #  Hour of the year
            # |--0h--|--1h--|--2h--|--3h--|--4h--|..
            #
            # #  Job interval = tr
            #   |<--------------------->|
            #   | t0 |  ti  |  ti  | tn |
            #           i1     i2

            tr = tend_hour - tbeg_hour
            t0 = tbeg_hour + 1 - tbeg
            tn = tend - tend_hour
            
            for h in range(tbeg_hour, tend_hour+1):
                hours.setdefault( h, [0, 0, 0, set()] )

            # Start and End in same hour
            if tr == 0:
                hours[tbeg_hour].append
                hours[tbeg_hour][3].add(host)
                hours[tbeg_hour][0] = len(hours[tbeg_hour][3])
                hours[tbeg_hour][1] += float(slots)*trun
                hours[tbeg_hour][2] += float(mem)
            # Start and End times in different hours
            if  tr >= 1:
                # Start hour
                hours[tbeg_hour][3].add(host)
                hours[tbeg_hour][0] = len(hours[tbeg_hour][3])
                hours[tbeg_hour][1] += float(slots)*t0
                hours[tbeg_hour][2] += float(mem)
                
                # End hour
                hours[tend_hour][3].add(host)
                hours[tend_hour][0] = len(hours[tend_hour][3])
                hours[tend_hour][1] += float(slots)*tn
                hours[tend_hour][2] += float(mem)
                
                if tr >= 2:
                    for h in range(tbeg_hour+1, tend_hour):
                        hours[h][3].add(host)
                        hours[h][0] = len(hours[h][3])
                        hours[h][1] += float(slots)
                        hours[h][2] += float(mem)

            # hkey = str(host)
            #nodes.setdefault(host, [0, 0])
            #nodes[host][0] += run_hours*float(slots)
            #nodes[host][1] += run_hours*float(mem)

print('Min Max Hour', minHour, maxHour)
print('Min Max Day ', minDay, maxDay)

#pp.pprint(nodes)
#pp.pprint(days)
#pp.pprint(hours)

for k,v in hours.items():
    print(k, v[0], round(v[1],2), round(v[2],2) )

# print(slots_by_hours)
# for i,v in np.ndenumerate(hours.nonzero()):
#    print(i,v )
# print(round(sumw,2))

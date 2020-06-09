#!/usr/bin/env python3

# Bhupender Thakur 2019

import argparse as ap
import datetime as dt
import pprint as pp
import numpy as np
import sys
import re
import traceback
from collections import OrderedDict as od


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

# now = dt.datetime.now()
# print(now)
# print(date_this_year)
# sys.exit()
# days = list(range(365))
days = od()
nodes = od()
hours = od()


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
        slots = line[34]

        tsub = float(line[8])/OneK
        tbeg = float(line[9])/OneK
        tend = float(line[10])/OneK

        wait_hours = round((tbeg-tsub)/3600., 2)
        run_hours = round((tend-tbeg)/3600., 2)

        # day = tbeg_this_year['day']
        # sec = tbeg_this_year['sec']

        failed = line[11]

        if tbeg == 0:
            print("error", day, jobid, queue, host, user, proj, failed)

        else:

            tsub_this_year = epoch_to_year(tsub)['sec']
            tbeg_this_year = epoch_to_year(tbeg)['sec']
            tend_this_year = epoch_to_year(tend)['sec']


            tbeg_hour = int(tbeg_this_year/3600.)
            tend_hour = int(tend_this_year/3600.)
            tbeg_day = int(tbeg_this_year/(3600.*24))
            tend_day = int(tend_this_year/(3600.*24))
            

            match = c_pattern.search(hres)
            if match:
                # print("matching", match.group(), match.start(), match.end())
                # print("matching", match[1], match[2])
                if match[2].lower() == 'g':
                    # print(match[1], 'g')
                    mem = float(slots)*float(match[1])
                elif match[2].lower() == 'm':
                    # print(match[1], 'm')
                    mem = (float(slots)*float(match[1]))/1000.
                else:
                    mem = 0.0
                # print("matching", hres[match.start(): match.end()])
                
            tdays = int(tend_day - tbeg_day + 1)
            tdelta = tend - tbeg

            if tend > tbeg:
                #
                for d in range(tbeg_day, tend_day+1):
                    days.setdefault(d, [0, 0])
                    days[d][0] += float(slots)*(run_hours)/float(tdays)
                    days[d][1] += int(mem)*(run_hours)/float(tdays)

                for h in range(tbeg_hour, tend_hour+1):
                    hours.setdefault(h, [0, 0])
                    hours[h][0] += int(slots)
                    hours[h][1] += int(mem)

                nodes.setdefault(host, [0, 0])
                nodes[host][0] += run_hours*float(slots)
                nodes[host][0] += run_hours*float(mem)
                

pp.pprint(nodes)
pp.pprint(days)
#pp.pprint(hours)

# print(slots_by_hours)
# for i,v in np.ndenumerate(hours.nonzero()):
#    print(i,v )
# print(round(sumw,2))

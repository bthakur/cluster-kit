#!/user/bin/env python

import matplotlib as mp
import matplotlib.pyplot as plt
from   matplotlib.dates import date2num , DateFormatter
import collections as cl

import numpy as np
from scipy.interpolate import interp1d
import datetime as dt

import pprint as pp
import sys

def global_values():
	global file_i, file_j
	file_i='Tmp_cycl'
	file_j='Tmp_disp'

def read_file(file_inp):
	with open(file_inp,'r') as fi:
		li=fi.readlines()
	return li

def main():
	global_values()
	a=read_file(file_i)
	b=read_file(file_j)
	d={}
	c={}
	dl=[]
	ds={}
	cs={}
        for i in a:
                t=i.split(' ')[0][0:18]
                dp=int(float(i.split(' ')[1]))
                # Assuming the date format in messages files doesnt change
                # month=t[0:2], day=[3:5], year=[6:10], min=[13:15], sc=[16:18]
                yy=t[6:10]; dd=t[3:5]; mm=t[0:2]; hh=t[10:12]; mn=t[13:15]; sc=t[16:18]
                k= dt.datetime(int(yy), int(mm), int(dd), int(hh), int(mn), int(sc))
                cs[k]=dp
		#print k, i.split(' ')[1],dp
		#print i,'--',i.split(' ')[0], i.split(' ')[1]
		
	for i in b:
		t=i.split(' ')[0][0:18]
		dp=int(float(i.split(' ')[1]))
		# Assuming the date format in messages files doesnt change
		# month=t[0:2], day=[3:5], year=[6:10], min=[13:15], sc=[16:18]
		yy=t[6:10]; dd=t[3:5]; mm=t[0:2]; hh=t[10:12]; mn=t[13:15]; sc=t[16:18]
		#print t
		#print yy, mm, dd, hh, mn,sc
		k= dt.datetime(int(yy), int(mm), int(dd), int(hh), int(mn), int(sc))
		ks= dt.datetime(int(yy), int(mm), int(dd), int(hh), int(mn), 0)
		d[k]=dp
		if ks in ds:
			ds[ks]+=dp
		else:
			ds[ks]=dp
		#print dt.datetime.now()
		#sys.exit()
	#yn_cor = interp1d(ds.keys(), dl, kind='cubic')
	ds=cl.OrderedDict(sorted(ds.items()))
	cs=cl.OrderedDict(sorted(cs.items()))
	#print pp.pprint(ds)
	fig, ax = plt.subplots()
	#ax.hist(ds.values(), bins=len(ds.keys()))
	#ax.plot(ds.keys(),ds.values(),'.-')
	ax.plot(cs.keys(),cs.values(),'.-')
	#plt.plot(xn_ax, yn_cor)
	ax.fmt_xdata = DateFormatter('%m-%d')
	ax.xaxis.set_major_formatter(DateFormatter('%a %d\n%b'))
	DateFormatter('%a %d\n%b')
	ax.autoscale_view()
	plt.show()

if __name__ == "__main__":
	main()


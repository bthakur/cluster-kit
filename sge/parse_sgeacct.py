#!/usr/bin/env python

import os, sys
import re


helptext="""
+-------+
| Usage :
+-------+
                    
  ./parse_sgeacct.py  -b Begin_date should be  atleast
                      -e End_date should be at most
                      -a At_this_time(Begin and End date must lie within)
                      -f Use accounting files(comma separated)
                      -z Use the zipped accounting files(, separated)
                      

  python       Without arguments, it runs pbsnodes on all nodes

  python  -h   Will print help message and exit

"""
def help():
    print helptext

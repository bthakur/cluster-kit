#!/usr/bin/env python

import os,sys,subprocess
import platform
import re

# Simple tool to help build packages

global pkg, pkg_top
#pkg_top='/opt/packages/'
pkg_top='/global/homes/b/bthakur/log/cluster-kit/soft/'
pkg={}
pkg{'name'}=""
pkg{'vers'}=""
pkg{'src'}={'loc': 'http://www.netlib.org/lapack/lapack-3.5.0.tgz', '
             put': pkg_top'+'','get'='['wget']', 'zipped'=True}
pkg{'conf'}={'pre':'[]', 'cfg':'[]', 'pos':'['make', 'install']'}
pkg{'make'}={'pre':'[]', 'mak':'[]', 'pos':'['make', 'install']'}
pkg{'test'}=''

#
#pkg_top="/usr/syscom/"
#pkg_sty="_"

def get_basebuild():
    distrb=platform.dist()
    complr=platform.python_compiler()
    tag=''
    for f in distrb,pkg_sty,complr:
        if type(f) != str:
            x=reduce(lambda x,y: x+y, list(f))
            tag=tag+x.replace(" ","")
        else:
            tag=tag+f.replace(" ","")
    return tag

def run_command(com_inp):
    com_out={}
    try:
        p=sp.Popen(com_inp,stdout=sp.PIPE, stderr=sp.PIPE)
    except:
        print "    %s did not return version" %com
    # some issues on carver python26 with p.wait
    out,err=p.communicate()
    com_out['ret']=p.returncode
    com_out['inp']=com_inp
    com_out['err']=err
    if p.returncode ==0 :
        com_out['out']=str.split(out,'\n')
    return com_out

def configure():
    print "Configure"
    #cfg_pfx
    #cfg_sty
    #cfg_cmp

def main():
    pkg_sub=get_basebuild()
    pkg_pfx=pkg_top+pkg_sub
    print "    Prefix %s" %pkg_pfx
    pkg
 

if __name__ == "__main__":
    main()


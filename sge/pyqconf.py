#!/usr/bin/env python

import re,os,subprocess

def check_opts():
#-# Options we can parse
    opts='-n:-a:-d:-h-'
    if  sys.argv:
        args=sys.argv[1:]
        optlist,arglist=getopt.getopt(args,opts)
        print "+-----------------+"
        print "| Options Supplied|"
        print "+-----------------+"
        print " %s" %optlist
        dic_arg={}
        #sys.exit()
        for o,a in optlist:
            dic_arg[o]=a
            #if o=='-f':
            #    print "Processing -f"
            #    #f_fopt=True
            #elif o=='-Q':
            #    f_Qopt=True
            #elif o=='-a':
            #    f_aopt=True
            #elif o=='-h':
            if o=='-h':
               help()
               sys.exit()
        print "dictionary",dic_arg

# +------------------------------------------------
# ! Transforms hosts to a flat list
# !   -n host[001-100:10,113]
# +------------------------------------------------
def process_nodes(a):
  # ! Transforms hosts to a flat list
  m0=hname_srch.search(a)
  cluster=a[m0.start():m0.end()]
  m1=nodes_list_srch.search(a)
  nodelist=a[m1.start():m1.end()]
  b=[]
  if m1:
    for x in nodelist.split(','):
      m2=split_nodes_srch.search(x)
      if m2:
        begin=m2.groups()[0]
	end=m2.groups()[1] if m2.groups()[1] else begin
        m4=intvl_srch.search(x)
        #print begin,end,x[m4.start()+1:m4.end()]
        intvl=int(x[m4.start()+1:m4.end()]) if m4 else 1
        pow=int(math.log(int(begin),10))
        for y in range(int(begin) ,int(end)+1,intvl):
          pow=int(math.log(y,10))+1
          node=cluster+begin[0:len(begin)-pow]+str(y)
          b.insert(0,str(node))
      else:
        m3=solo_node_srch.search(x)
        #print 'solo',m3
        if m3:
          node=cluster+x[m3.start():m3.end()]
          b.insert(0,node)
  if b==[]:
    print "No useful nodes found with -n "
  # sys.exit()
  return b

#----------------------------
# Main
#----------------------------

def main():
    global f_sge, default_acct
    check_sge()
    check_opts()
    #read_accounting()
    #print list_of_files

if __name__ == "__main__":
    main()


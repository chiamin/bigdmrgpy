import os
import subprocess as sp

def exe (command):
  #print command
  return sp.Popen(command, shell=True, stdout=sp.PIPE).communicate()[0]

def getid ():
  ids = []
  queue = exe ('myqueue.sh')
  lines = queue.split('\n')
  for line in lines:
    if 'chiamic' in line:
      jobid = line.split()[0]
      ids.append (jobid)
  return ids

def get_node_id (queues):
    dat = sp.check_output(('sinfo'))
    dat = dat.rstrip().split('\n')

    nodes = []
    for line in dat[1:]:
        tmp = line.split()
        queue = tmp[0]
        if queue in queues and 'down' not in line:
            tmp = tmp[-1].rstrip(']').split(']')
            for nodestr in tmp:
                nodestr = nodestr.lstrip(',')

                if '[' not in nodestr:
                    if ',' not in nodestr:
                        nodes.append (nodestr)
                    else:
                        for node in nodestr.split(','):
                            nodes.append (node)
                    break

                prefix,idtmp = nodestr.split('[')

                if ',' in prefix:
                    ptmp = prefix.split(',')
                    for node in ptmp[:-1]:
                        nodes.append (node)
                    prefix = ptmp[-1]

                idstr = idtmp.split(',')
                for ids in idstr:
                    if '-' not in ids:
                        nodes.append (prefix+ids)
                    else:
                        ibeg,iend = map(int,ids.split('-'))
                        for i in xrange(ibeg,iend+1):
                            nodes.append (prefix+str(i))
    return nodes

if __name__ == '__main__':

  workdir = '/work/chiamic/'

  jobs = getid()

  queues = ['mf_brd2.4', 'mf_i-b2.8', 'mf_nes2.8', 'mf_ilg2.3', 'mf_m-c1.9', 'mf_m-c2.2', 'c6145']
  nodes = get_node_id (queues)

  todel=[]
  for node in nodes:
    try: dirs = sp.check_output(('ssh',node,'ls',workdir))
    except: dirs = ''
    if dirs == '':
      print 'In '+node+': '
    else:
      print 'In '+node+': '+workdir+':'
      for dirr in dirs.split():
        #print '  ', dirr
        if dirr in jobs:
          print '  Jobs running: ', dirr
        else:
          print '  Trash: ', dirr
          todel.append ([node, dirr])
    exe ('exit')

  if len(todel) != 0:
    print
    print 'Trash data:'
    for dd in todel: print '  ',dd[1]
    ifdel = raw_input ('Delete trash data? [y/n] ')
    if ifdel == 'y' or ifdel == 'Y':
      for node,dirr in todel:
        exestr = 'ssh '+node+' rm -r '+workdir+'/'+dirr
        print exestr
        os.system (exestr)

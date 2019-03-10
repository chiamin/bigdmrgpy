import sys
sys.path.append('/home/chiamic/mypy')
import numpy as np
from qninput import specialqns

#------------ define delta patterns ---------------
def delta_all (lx,ly,delta,ypbc):
  dels = []
  for y in xrange(1,ly+1):
    for x in xrange(1,lx+1):
      # horizontal bonds
      if x != lx:
        dels.append ([x,y,x+1,y,delta])
      # vertical bonds
      if y == ly:
        if ypbc:
          y2 = 1
          dels.append ([x,y,x,y2,-delta])
      else:
          y2 = y+1
          dels.append ([x,y,x,y2,-delta])
  return dels,'delta.all_'+str(delta)

def delta_block (lx,ly,x1,x2,delta,ypbc):
  dels = []
  for y in xrange(1,ly+1):
    for x in xrange(1,lx+1):
      if x >= x1 and x <= x2:
        # horizontal bonds
        if x != lx:
          dels.append ([x,y,x+1,y,delta])
        # vertical bonds
        if y == ly:
          if ypbc:
            y2 = 1
            dels.append ([x,y,x,y2,-delta])
        else:
            y2 = y+1
            dels.append ([x,y,x,y2,-delta])
  return dels,'delta.block_x'+str(x1)+'_x'+str(x2)

def delta_edges (lx,ly,delta,x=1,oneedge=False,yperiodic=True,xedge=False):
  dels = []
  for y in xrange(1,ly+1):
    if xedge:
      # left x bonds
      x2,y2 = x+1,y
      dels.append ([x,y,x2,y2,delta])
      if not oneedge:
        # right x bonds
        x,x2,y2 = lx-1,lx,y
        dels.append ([x,y,x2,y2,delta])

    if y == ly:
      if yperiodic:
        # left y bonds
        x2,y2 = x,1
        dels.append ([x,y,x2,y2,-delta])
	if not oneedge:
          # right y bonds
          x,x2,y2 = lx,lx,1
          dels.append ([x,y,x2,y2,-delta])
    else:
      # left y bonds
      x2,y2 = x,y+1
      dels.append ([x,y,x2,y2,-delta])
      if not oneedge:
        # right y bonds
        x = lx+1-x
        x2,y2 = x,y+1
        dels.append ([x,y,x2,y2,-delta])
  if xedge: dname = 'delta'+str(delta)+'.xyedge'
  else: dname = 'delta'+str(delta)+'.yedge'
  if oneedge: dname += '1'
  else: dname += '2'
  return dels,dname

#----------- end of delta patterns ---------------


def setdel (para,deltas,firstsweep=-1):
  i = 0
  while i < len(para):
    # Read lx, ly
    if 'lx =' in para[i]:
      temp = para[i].split()
      lx = int(temp[-1])
    elif 'ly =' in para[i]:
      temp = para[i].split()
      ly = int(temp[-1])

    if firstsweep > 0 and 'firstmainsweep =' in para[i]:
        para[i] = '\tfirstmainsweep = '+str(firstsweep)+'\n'

    # delta potential
    if 'delta_potential' in para[i]:
      para[i] = '    delta_potential\n'
      while 'allbonds' not in para[i]: i += 1
      para[i] = '        allbonds = no\n'
      while 'numpair' not in para[i]: i += 1
      para[i] = '        numpair = '+str(len(deltas))+'\n'
      # delete current values
      while ' bonds' not in para[i]: i += 1
      i += 3
      while '}' not in para[i]: del para[i]
      # add new values
      for bond in deltas:
        x1,y1,x2,y2,delta = bond[0],bond[1],bond[2],bond[3],bond[4]
        para.insert (i,'            '+str(x1)+'  '+str(y1)+'  '+str(x2)+'  '+str(y2)+'  '+str(delta)+'\n')
        i += 1
    # set modham
    if 'modham' in para[i]:
      para[i] = '    modham\n'
      while 'numchange' not in para[i]: i += 1
      para[i] = '        numchange = 1\n'
      # delete current values
      while 'coefs' not in para[i]: i += 1
      i += 3
      while '}' not in para[i]: del para[i]
      # set
      para.insert (i,'            1   1.00\n')
      i += 1
    i += 1
  return para


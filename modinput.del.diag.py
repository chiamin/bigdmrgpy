import sys
sys.path.append('/home/chiamic/mypy')
import numpy as np
from qninput import specialqns

periodic = 1

def main():
  parafile = sys.argv[1]
  para = list(open(parafile))
  setdel ('edge d-wave',para) # can be 'all d-wave' or 'edge d-wave'
  write (parafile,para)

def diag_bond_type (x1,y1,x2,y2,ly=-1):
# giving ly means including periodic boundary bonds in y direction
  if ly != -1:
    # periodic bonds in y direction
    if y1 == 1 and y2 == ly:
      if x2 == x1-1: return '/'
      elif x2 == x1+1: return '\\'
      else: raise Exception
    elif y1 == ly and y2 == 1:
      if x2 == x1-1: return '\\'
      elif x2 == x1+1: return '/'
      else: raise Exception
  if y1 == y2:
    if abs(x1-x2) == 1:
      x = min([x1,x2])
      if x % 2 == 1: return '/'
      else: return '\\'
    else: raise Exception
  elif y2 == y1+1:
    if x2 == x1-1: return '\\'
    elif x2 == x1+1: return '/'
    else: raise Exception
  elif y2 == y1-1:
    if x2 == x1-1: return '/'
    elif x2 == x1+1: return '\\'
    else: raise Exception
  else:
    raise Exception

# mode could be: all d-wave
def setdel (mode,para):
  i = 0
  while i < len(para):
    # Read lx, ly
    if 'lx =' in para[i]:
      temp = para[i].split()
      lx = int(temp[-1])
    elif 'ly =' in para[i]:
      temp = para[i].split()
      ly = int(temp[-1])
    #elif 'periodic = ' in para[i]:
    #  temp = para[i].split()
    #  periodic = int(temp[-1])
    # delta potential
    if 'delta_potential' in para[i]:
      para[i] = '    delta_potential\n'
      while 'allbonds' not in para[i]: i += 1
      para[i] = '        allbonds = no\n'
      while 'numpair' not in para[i]: i += 1
      nidx = i
      # delete current values
      while ' bonds' not in para[i]: i += 1
      i += 3
      while '}' not in para[i]: del para[i]
      # add new values
      bonds = []
      if mode == 'all d-wave':
        for yi in xrange(1,ly+1):
          for xi in xrange(1,lx):
            bonds.append ([xi,yi,xi+1,yi])
        for xi in xrange(1,lx,2):
          for yi in (xrange(2,ly+1)):
            bonds.append ([xi,yi,xi+1,yi-1])
          if periodic:
              bonds.append ([xi,1,xi+1,ly])
        for xi in xrange(2,lx,2):
          for yi in xrange(1,ly):
            bonds.append ([xi,yi,xi+1,yi+1])
          if periodic:
            bonds.append ([xi,ly,xi+1,1])
      elif mode == 'edge d-wave':
        for yi in xrange(1,ly+1):
          bonds.append ([1,yi,2,yi])
          bonds.append ([lx-1,yi,lx,yi])
          if yi != 1:
            bonds.append ([1,yi,2,yi-1])
            bonds.append ([lx-1,yi,lx,yi-1])
        if periodic:
          bonds.append ([1,1,2,ly])
          bonds.append ([lx-1,1,lx,ly])
      for bond in bonds:
        x1,y1,x2,y2 = bond[0],bond[1],bond[2],bond[3]
        try: btype = diag_bond_type (x1,y1,x2,y2,ly)
        except:
          print 'Error: bond =',x1,y1,x2,y2
          raise Exception
        if btype == '/':
          para.insert (i,'            '+str(x1)+'  '+str(y1)+'  '+str(x2)+'  '+str(y2)+'  1.0\n')
        elif btype == '\\':
          para.insert (i,'            '+str(x1)+'  '+str(y1)+'  '+str(x2)+'  '+str(y2)+'  -1.0\n')
        else:
          print 'Error: btype =',btype
          raise Exception
        i += 1
      # set numpair
      para[nidx] = '        numpair = '+str(len(bonds))+'\n'
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

def write (name,dat):
  f = open(name, 'w')
  for di in dat: f.write(di)
  f.close()

main()

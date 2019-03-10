import sys
sys.path.append('/home/chiamic/mypy')
import numpy as np
from qninput import specialqns

periodic = 1

def main():
  parafile = sys.argv[1]
  para = list(open(parafile))
  setorder ('zigzag',para) # can be 'all d-wave' or 'edge d-wave'
  write (parafile,para)

# mode: 'zigzag'
def setorder (mode,para):
  i = 0
  while i < len(para):
    # Read lx, ly
    if 'lx =' in para[i]:
      temp = para[i].split()
      lx = int(temp[-1])
    elif 'ly =' in para[i]:
      temp = para[i].split()
      ly = int(temp[-1])
    # new order
    if 'neworder' in para[i]:
      para[i] = '    neworder\n'
      # delete current values
      i += 3
      while '}' not in para[i]: del para[i]
      # add new values
      if mode == 'zigzag':
        neworder = diag_zigzag_path (lx,ly)
      for order in neworder:
        x,y = order[0], order[1]
        para.insert (i,'        '+str(x)+'  '+str(y)+'\n')
        i += 1
    i += 1
  return para

def goto (x,y,dirr):
  if dirr == '/up':
    if x % 2 == 1:
      return x+1, y
    else:
      return x+1, y+1
  elif dirr == '\\up':
    if x % 2 == 1:
      return x-1, y
    else:
      return x-1, y+1
  elif dirr == '/dn':
    if x % 2 == 1:
      return x-1, y-1
    else:
      return x-1, y
  elif dirr == '\\dn':
    if x % 2 == 1:
      return x+1, y-1
    else:
      return x+1, y

def diag_zigzag_path (lx,ly):
  paths = []
  for x in xrange(1,lx,2):
    y = 1
    paths.append ([x,y])
    while True:
      x,y = goto (x,y,'/up')
      paths.append ([x,y])
      x,y = goto (x,y,'\\up')
      if y > ly: break
      paths.append ([x,y])
  return paths

def write (name,dat):
  f = open(name, 'w')
  for di in dat: f.write(di)
  f.close()

main()

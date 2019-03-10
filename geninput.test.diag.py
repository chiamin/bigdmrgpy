import sys
sys.path.append('/home/chiamic/mypy')
import numpy as np
from qninput import specialqns

lx = 32
ly = 3
tx = 1.0
ty = 0.0
U = 8.0
J = 0.0
V = 0.0
Sz = 0
mu = 1.56
#n = 0.875

holes = 12
# holeloc could be 0 or [[x1,y1],[x2,y2],...]
holeloc = 0#\
[\
[4,1],[4,2],[4,3],\
[12,1],[12,2],[12,3],\
[20,1],[20,2],[20,3],\
[28,1],[28,2],[28,3]\
]

if holeloc != 0:
  if len(holeloc) != holes:
    print 'hole location not match'
    exit()
  qninit = specialqns (lx,ly,holes,holeloc)
N = lx*ly-holes
n = N/float(lx*ly)

localh = 'localmu' # pattern, localmu
hfield = 0.25
#          1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48
pattern = [1,-1, 1, 0,-1, 1,-1, 1,-1, 1,-1, 0, 1,-1, 1,-1, 1,-1, 1, 0,-1, 1,-1, 1,-1, 1,-1, 0, 1,-1, 1,-1]#, 1,-1, 1, 0,-1, 1,-1, 1,-1, 1,-1, 0, 1,-1, 1,-1]
permh_xloc = []

firstmainsweep = 0
if localh == 'pattern': firstmainsweep = 8

### For localh == localmu
minmu, maxmu = 0., 0.2
dmu = (maxmu - minmu) / float(lx-1)
mu_set = [minmu + i*dmu for i in xrange(lx)]

cdagc = 0
SplusSminus = 0
mtable = [
#	    maxstates minstates	numstr	target  noise   eps	maxiter dim	trim
'	    64		64	64	1e-10	0.0	1e-4	1	10	0',
'	    128		128	128	1e-10	0.0	1e-6	1	8	0',
'	    200		200	200	1e-12	0.0	1e-4	1	7	0',
'	    300		300	300	1e-12	0.0	1e-4	1	6	0',
'	    300		300	300	1e-12	0.0	1e-4	1	6	0',
'	    500		500	500	1e-12	0.0	1e-4	1	5	0',
'	    500		500	500	1e-12	0.0	1e-4	1	5	0',
'	    800		800	800	1e-12	0.0	1e-4	1	5	0',
'	    800		800	800	1e-12	0.0	1e-4	1	5	0',
'	    1400	1400	1400	1e-12	0.0	1e-4	1	4	0',
'	    1400	1400	1400	1e-12	0.0	1e-4	1	4	0',
'	    2400	2400	2400	1e-12	0.0	1e-4	1	4	0',
'	    2400	2400	2400	1e-12	0.0	1e-4	1	4	0',
'	    4000	4000	4000	1e-12	0.0	1e-4	1	4	0',
'	    4000	4000	4000	1e-12	0.0	1e-4	1	4	0',
'           5500        5500    5500    1e-12   0.0     1e-4    1       4       0',
'           5500        5500    5500    1e-12   0.0     1e-4    1       4       0',
'           8500        8500    8500    1e-12   0.0     1e-4    1       4       0',
'           8500        8500    8500    1e-12   0.0     1e-4    1       4       0',
'	    12000	12000	12000	1e-12	0.0	1e-4	1	3	0',
'	    12000	12000	12000	1e-12	0.0	1e-4	1	3	0',
'           17000       17000   17000   1e-12   0.0     1e-4    1       3       0',
'           17000       17000   17000   1e-12   0.0     1e-4    1       3       0',
'           21000       21000   21000   1e-12   0.0     1e-4    1       3       0',
'           21000       21000   21000   1e-12   0.0     1e-4    1       3       0',
'           25000       25000   25000   1e-12   0.0     1e-4    1       3       0',
'           25000       25000   25000   1e-12   0.0     1e-4    1       3       0',
'           30000       30000   30000   1e-12   0.0     1e-4    1       3       0',
'           30000       30000   30000   1e-12   0.0     1e-4    1       3       0',
'           35000       35000   35000   1e-12   0.0     1e-4    1       3       0',
'           35000       35000   35000   1e-12   0.0     1e-4    1       3       0',
'           40000       40000   40000   1e-12   0.0     1e-4    1       3       0',
'           40000       40000   40000   1e-12   0.0     1e-4    1       3       0',
]
if type(N) != int:
  if not  N.is_integer():
    print 'Error: N is not an integer'
    exit()
N = int(N)
if n.is_integer(): n = int(n)
numsweeps = len(mtable)
base = '/home/chiamic/hubbard_U8_n0875/huben.sample'
base = list(open(base))

def setval (lx,ly,tx,ty,U,J,V,Sz,N,firstmainsweep,numsweeps,mtable,para):
  i = 0
  while i < len(para):
    if 'lx =' in para[i]: para[i] = '\tlx = '+str(lx)+'\n'
    elif 'ly =' in para[i]: para[i] = '\tly = '+str(ly)+'\n'
    elif 'periodic =' in para[i]: para[i] = '        periodic = 0\n'
    elif 'tx =' in para[i]: para[i] = '    tx = '+str(tx)+'\n'
    elif 'ty =' in para[i]: para[i] = '    ty = '+str(ty)+'\n'
    elif 'U =' in para[i]: para[i] = '    U = '+str(U)+'\n'
    elif 'J =' in para[i]: para[i] = '    J = '+str(J)+'\n'
    elif 'V =' in para[i]: para[i] = '    V = '+str(V)+'\n'
    elif 'mu =' in para[i]: para[i] = '    mu = '+str(mu)+'\n'
    elif 'Sz =' in para[i]: para[i] = '\tSz = '+str(Sz)+'\n'
    elif 'Nf =' in para[i]:
      if mu == 0: para[i] = '\tNf = '+str(N)+'\n'
      else: para[i] = '\tNf = 0\n'
    elif 'firstmainsweep =' in para[i]: para[i] = '\tfirstmainsweep = '+str(firstmainsweep)+'\n'
    elif 'numsweeps =' in para[i]: para[i] = '\tnumsweeps = '+str(numsweeps)+'\n'
    # extrabonds
    elif 'extrabonds' in para[i]:
      para[i] = '    extrabonds\n'
      while 'numbonds' not in para[i]: i += 1
      para[i] = '        numbonds = '+str((lx-1)*ly)+'\n'
      # delete current values
      while ' bonds' not in para[i]: i += 1
      i += 3
      while '}' not in para[i]: del para[i]
      # add new values
      for xi in range(1,lx,2):
        for yi in (range(2,ly+1)):
          para.insert (i,str(xi)+' '+str(yi)+' '+str(xi+1)+' '+str(yi-1)+' 1 0\n')
          i += 1
        para.insert (i,str(xi)+' 1 '+str(xi+1)+' '+str(ly)+' 1 0\n')
        i += 1
      for xi in range(2,lx,2):
        for yi in range(1,ly):
          para.insert (i,str(xi)+' '+str(yi)+' '+str(xi+1)+' '+str(yi+1)+' 1 0\n')
          i += 1
        para.insert (i,str(xi)+' '+str(ly)+' '+str(xi+1)+' 1 1 0\n')
        i += 1
    # localfields
    elif 'localfields' in para[i]: para[i] = '    localfieldsX\n'
    # localmuh
    elif 'localmuh' in para[i]:
      if not localh: para[i] = '    localmuhX\n'
      else:
        para[i] = '    localmuh\n'
        numh = 0 # number of sites with local field
        # store index of 'numsite'
        while 'numsite' not in para[i]: i += 1
        nidx = i
        # delete current values
        while 'sites' not in para[i]: i += 1
        i += 3
        while '}' not in para[i]: del para[i]
        # add new values
        if localh == 'edgeh' or localh == 'edgeh2':
          for xi in [1,lx]:
            for yi in range(1,ly+1):
              if xi % 2 == yi % 2: hi = 0.25
              else: hi = -0.25
              if localh == 'edgeh2' and xi == lx: hi = -hi
              para.insert (i,'            '+str(xi)+'   '+str(yi)+'       2       0       '+str(hi)+'\n')
              i += 1
              numh += 1
        elif localh == 'pattern':
          for x in xrange(lx):
	    code = 0
            if x+1 in permh_xloc: code = 2
            if pattern[x] == 0: mui = -2
            else: mui = 0
            for y in xrange(ly):
              para.insert(i,'     \t'+str(x+1)+'\t'+str(y+1)+'\t'+str(code)+'\t'+str(mui)+'\t'+str(pattern[x]*hfield)+'\n')
              i += 1
              numh += 1
        elif localh == 'holeloc':
          for x in xrange(lx):
            code = 0
            if x+1 in permh_xloc: code = 2
            for y in xrange(ly):
              if [x+1,y+1] in holeloc: mui = -2
              else: mui = 2
              para.insert(i,'     \t'+str(x+1)+'\t'+str(y+1)+'\t'+str(code)+'\t'+str(mui)+'\t'+str(((-1)**y)*pattern[x]*0.25)+'\n')
              i += 1
              numh += 1
        elif localh == 'localmu':
          code = 2
          for x in xrange(lx):
            for y in xrange(ly):
              para.insert(i,'     \t'+str(x+1)+'\t'+str(y+1)+'\t'+str(code)+'\t'+str(mu_set[x])+'\t 0\n')
              i += 1
              numh += 1

        # set numsite
        para[nidx] = '        numsite = '+str(numh)+'\n'
    # m table
    elif '\tsweeps' in para[i]:
      # delete current values
      i += 3
      while '}' not in para[i]: del para[i]
      # add new values
      for mi in mtable:
        para.insert (i,mi+'\n')
        i += 1
    elif 'docdagc' in para[i]:
      if cdagc: para[i] = '    docdagc\n'
      else: para[i] = '    docdagcX\n'
    elif 'doSplusSminus' in para[i]:
      if SplusSminus: para[i] = '    doSplusSminus\n'
      else: para[i] = '    doSplusSminusX\n'
    # specialqns
    elif 'specialqns' in para[i]:
      if holeloc == 0:
        para[i] = '        specialqnsXX\n'
      else:
        para[i] = '        specialqns\n'
        while 'numspecial' not in para[i]: i += 1
        para[i] = '            numspecial = '+str(len(qninit))+'\n'
        i += 4
        while '}' not in para[i]: del para[i] 
        for qni in qninit:
          para.insert (i,qni+'\n')
          i += 1
    i += 1
  return para

def write (name,dat):
  f = open(name, 'w')
  for di in dat: f.write(di)
  f.close()

para = setval(lx=lx, ly=ly, tx=tx, ty=ty, U=U, J=J, V=V, Sz=Sz, N=N, firstmainsweep=firstmainsweep, numsweeps=numsweeps, mtable=mtable, para=base)
ofname = 'huben'+str(lx)+'x'+str(ly)+'.U'+str(U).rstrip('0').rstrip('.')+'.n'+str(n)+'.tp0.diag.in'
#ofname = 'h'+str(lx)+'x'+str(ly)+'ty'+str(ty)+'.in'
#ofname = 'huben'+str(lx)+'x'+str(ly)+'.U'+str(U).rstrip('0').rstrip('.')+'.N'+str(N)+'.tp0.in'
if localh == 'edgeh': ofname = ofname[:-2]+'edgeh.in'
elif localh == 'edgeh2': ofname = ofname[:-2]+'edgeh2.in'
elif localh == 'garnet': ofname = ofname[:-2]+'gnt.in'
elif localh == 'holes': ofname = ofname[:-2]+'holes.in'
elif localh == 'hh': ofname = ofname[:-2]+'hh.in'
elif localh == 'try': ofname = ofname[:-2]+'try.in'
elif localh == 'pattern':
  ofname = ofname[:-2]+'pattern.in'
  if permh_xloc != []: ofname = ofname[:-2]+'edgeh.in'
elif localh == 'holeloc': ofname = ofname[:-2]+'holeloc.in'
write (ofname,para)

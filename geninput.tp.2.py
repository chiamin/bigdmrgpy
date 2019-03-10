import numpy as np

lx = 16
ly = 6
tx = 1.0
ty = 1.0
tp = -0.2
U = 12.0
J = 0.0
V = 0.0
Sz = 0
n = 1.
N = lx*ly*n
localh = 'edge'  # could be 0, 'edge', 'garnet' or 'holes' or 'hh' or 'try'
### localh paterns
garnet = np.array([\
[ 0.05, -0.01, -0.05,  0.1, -0.05,  0.01,  0.05, -0.1],\
[-0.05,  0.01,  0.05, -0.1,  0.05, -0.01, -0.05,  0.1]\
])
holes = 6*np.array([-0.055,-0.1,-0.16,-0.18,-0.18,-0.16,-0.1,-0.055])
tinyh = 20*np.array([\
[ 0.006, -0.002, -0.002,  0.006, -0.006,  0.002,  0.002, -0.006],\
[-0.006,  0.002,  0.002, -0.006,  0.006, -0.002, -0.002,  0.006]\
])
tryh = [\
[ 0.2, -0.16,  0.036,  0.08, -0.2,  0.24, -0.2,  0.08,  0.08, -0.2,  0.24, -0.2,  0.08,  0.036, -0.16,  0.2],\
[-0.2,  0.16, -0.036, -0.08,  0.2, -0.24,  0.2, -0.08, -0.08,  0.2, -0.24,  0.2, -0.08, -0.036,  0.16, -0.2]\
]
### end
firstmainsweep = 0
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
'	    7000	7000	7000	1e-12	0.0	1e-4	1	4	0',
'	    7000	7000	7000	1e-12	0.0	1e-4	1	4	0',
#'           8500        8500    8500    1e-12   0.0     1e-4    1       4       0',
#'           8500        8500    8500    1e-12   0.0     1e-4    1       4       0',
'	    10000	10000	10000	1e-12	0.0	1e-4	1	3	0',
'	    10000	10000	10000	1e-12	0.0	1e-4	1	3	0',
#'	    12000	12000	12000	1e-12	0.0	1e-4	1	3	0',
#'	    12000	12000	12000	1e-12	0.0	1e-4	1	3	0',
'	    15000	15000	15000	1e-12	0.0	1e-4	1	3	0',
'	    15000	15000	15000	1e-12	0.0	1e-4	1	3	0',
#'           17000       17000   17000   1e-12   0.0     1e-4    1       3       0',
#'           17000       17000   17000   1e-12   0.0     1e-4    1       3       0',
#'           19000       19000   19000   1e-12   0.0     1e-4    1       3       0',
#'           19000       19000   19000   1e-12   0.0     1e-4    1       3       0',
#'           21000       21000   21000   1e-12   0.0     1e-4    1       3       0',
#'           21000       21000   21000   1e-12   0.0     1e-4    1       3       0',
#'           23000       23000   23000   1e-12   0.0     1e-4    1       3       0',
#'           23000       23000   23000   1e-12   0.0     1e-4    1       3       0',
#'           25000       25000   25000   1e-12   0.0     1e-4    1       3       0',
#'           25000       25000   25000   1e-12   0.0     1e-4    1       3       0',
#'           27000       27000   27000   1e-12   0.0     1e-4    1       3       0',
#'           27000       27000   27000   1e-12   0.0     1e-4    1       3       0',
#'           29000       29000   29000   1e-12   0.0     1e-4    1       3       0',
#'           29000       29000   29000   1e-12   0.0     1e-4    1       3       0'
]
if type(N) != int:
  if not  N.is_integer():
    print 'Error: N is not an integer'
    exit()
N = int(N)
if n.is_integer(): n = int(n)
numsweeps = len(mtable)
base = '/home/chiamic/hubbard/huben.sample'
base = list(open(base))

def setval (lx,ly,tx,ty,U,J,V,Sz,N,firstmainsweep,numsweeps,mtable,para):
  i = 0
  while i < len(para):
    if 'lx =' in para[i]: para[i] = '\tlx = '+str(lx)+'\n'
    elif 'ly =' in para[i]: para[i] = '\tly = '+str(ly)+'\n'
    elif 'tx =' in para[i]: para[i] = '    tx = '+str(tx)+'\n'
    elif 'ty =' in para[i]: para[i] = '    ty = '+str(ty)+'\n'
    elif 'U =' in para[i]: para[i] = '    U = '+str(U)+'\n'
    elif 'J =' in para[i]: para[i] = '    J = '+str(J)+'\n'
    elif 'V =' in para[i]: para[i] = '    V = '+str(V)+'\n'
    elif 'Sz =' in para[i]: para[i] = '\tSz = '+str(Sz)+'\n'
    elif 'Nf =' in para[i]: para[i] = '\tNf = '+str(N)+'\n'
    elif 'firstmainsweep =' in para[i]: para[i] = '\tfirstmainsweep = '+str(firstmainsweep)+'\n'
    elif 'numsweeps =' in para[i]: para[i] = '\tnumsweeps = '+str(numsweeps)+'\n'
    elif 'periodic =' in para[i]: para[i] = '        periodic = 0\n'
    # tprime
    elif 'extrabonds' in para[i]:
      para[i] = '    extrabonds\n'
      while 'numbonds' not in para[i]: i += 1
      para[i] = '        numbonds = '+str((lx*ly-ly)*2+lx)+'\n'
      # delete current values
      while ' bonds' not in para[i]: i += 1
      i += 3
      while '}' not in para[i]: del para[i]
      # add new values
      def addtp (i,x,y,xj,yj):
        if yj <= 0:
          yj = ly
          ttp = -tp
        elif yj > ly:
          yj = 1
          ttp = -tp
        else: ttp = tp
        para.insert (i,str(x)+' '+str(y)+' '+str(xj)+' '+str(yj)+' '+str(ttp)+' 0\n')
        i += 1
        return i
      for xi in range(1,lx):
        for yi in range(1,ly+1):
          # next nearest hopping
          i = addtp (i,xi,yi,xi+1,yi+1)
          i = addtp (i,xi,yi,xi+1,yi-1)
      for xi in range(1,lx+1):
        # -1 phase
        para.insert (i,str(xi)+' 1 '+str(xi)+' '+str(ly)+' -1 0\n')
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
        if localh == 'edge':
          for xi in [1,lx]:
            for yi in range(1,ly+1):
              if xi % 2 == yi % 2: hi = 0.25
              else: hi = -0.25
              para.insert (i,'            '+str(xi)+'   '+str(yi)+'       2       0       '+str(hi)+'\n')
              i += 1
              numh += 1
        elif localh == 'garnet':
          for xi in range(1,lx+1):
            if xi == 1 or xi == lx: code = 2
            else: code = 0
            for yi in range(1,ly+1):
              hi = garnet [(yi-1)%2][(xi-1)%8]
              para.insert (i,'            '+str(xi)+'   '+str(yi)+'       0       0       '+str(hi)+'\n')
              i += 1
              numh += 1
        elif localh == 'holes':
          for xi in range(1,lx+1):
            for yi in range(1,ly+1):
              para.insert (i,'            '+str(xi)+'   '+str(yi)+'       0       '+str(holes[xi-1])+'       0\n')
              i += 1
              numh += 1
        elif localh == 'hh':
          for xi in range(1,lx+1):
            for yi in range(1,ly+1):
              hi = tinyh [(yi-1)%2][(xi-1)%8]
              para.insert (i,'            '+str(xi)+'   '+str(yi)+'       0       '+str(holes[xi-1])+'       '+str(hi)+'\n')
              i += 1
              numh += 1
        elif localh == 'try':
          for xi in range(1,lx+1):
            for yi in range(1,ly+1):
              hi = tryh [(yi-1)%2][(xi-1)%16]
              if xi == 1 or xi == lx: code = 2
              else: code = 0
              para.insert (i,'            '+str(xi)+'   '+str(yi)+'       '+str(code)+'       0       '+str(hi)+'\n')
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

    i += 1
  return para

def write (name,dat):
  f = open(name, 'w')
  for di in dat: f.write(di)
  f.close()

para = setval(lx=lx, ly=ly, tx=tx, ty=ty, U=U, J=J, V=V, Sz=Sz, N=N, firstmainsweep=firstmainsweep, numsweeps=numsweeps, mtable=mtable, para=base)
ofname = 'huben'+str(lx)+'x'+str(ly)+'.U'+str(U).rstrip('0').rstrip('.')+'.n'+str(n)+'.tp'+str(tp)+'.nt.phase.in'
#ofname = 'h'+str(lx)+'x'+str(ly)+'ty'+str(ty)+'.in'
#ofname = 'huben'+str(lx)+'x'+str(ly)+'.U'+str(U).rstrip('0').rstrip('.')+'.N'+str(N)+'.tp0.in'
if localh == 'edge': ofname = ofname[:-2]+'edgeh.in'
elif localh == 'garnet': ofname = ofname[:-2]+'gnt.in'
elif localh == 'holes': ofname = ofname[:-2]+'holes.in'
elif localh == 'hh': ofname = ofname[:-2]+'hh.in'
elif localh == 'try': ofname = ofname[:-2]+'try.in'
write (ofname,para)

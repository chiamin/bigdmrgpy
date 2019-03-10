
lx = 16
ly = 6
tx = 1.0
ty = 0.0
tp = -0.2
U = 12.0
J = 0.0
V = 0.0
Sz = 0
n = 1.
N = lx*ly*n
#N = (lx*ly)-1
edgeh = 1
zsweep = False
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
'	    10000	10000	10000	1e-12	0.0	1e-4	1	3	0',
'	    10000	10000	10000	1e-12	0.0	1e-4	1	3	0',
'	    15000	15000	15000	1e-12	0.0	1e-4	1	3	0',
'	    15000	15000	15000	1e-12	0.0	1e-4	1	3	0',
]
if type(N) != int:
  if not  N.is_integer():
    print 'Error: N is not an integer'
    exit()
N = int(N)
if n.is_integer(): n = int(n)
numsweeps = len(mtable)
base = '/home/chiamic/hubbard/huben.tilted.sample'
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
    # localfields
    elif 'localfields' in para[i]:
      if edgeh == 0:
        para[i] = '    localfieldsX\n'
      else:
        para[i] = '    localfields\n'
        while 'numsite' not in para[i]: i += 1
        para[i] = '\tnumsite = '+str(2*ly)+'\n'
        # delete current values
        while 'sites' not in para[i]: i += 1
        i += 3
        while '}' not in para[i]: del para[i]
        # add new values
        if edgeh == 1: edgefield = [0.25,-0.25]
        elif edgeh == 2: edgefield = [0.25,0.25]
        for xi,Hi in zip([1,lx],edgefield):
          for yi in range(1,ly+1):
            para.insert (i,'\t    '+str(xi)+'\t'+str(yi)+'\t0\t'+str(Hi)+'\t'+str(U)+'\n')
            i += 1
    # extrabonds
    elif 'extrabonds' in para[i]:
      while 'numbonds' not in para[i]: i += 1
      para[i] = '        numbonds = '+str((lx-1)*ly+2*(lx*ly-ly))+'\n'
      # delete current values
      while ' bonds' not in para[i]: i += 1
      i += 3
      while '}' not in para[i]: del para[i]
      # add new values: tilted y
      for xi in range(1,lx,2):
        for yi in (range(2,ly+1)):
          para.insert (i,str(xi)+' '+str(yi)+' '+str(xi+1)+' '+str(yi-1)+' 1 0\n')
          i += 1
        para.insert (i,str(xi)+' 1 '+str(xi+1)+' '+str(ly)+' -1 0\n')
        i += 1
      for xi in range(2,lx,2):
        for yi in range(1,ly):
          para.insert (i,str(xi)+' '+str(yi)+' '+str(xi+1)+' '+str(yi+1)+' 1 0\n')
          i += 1
        para.insert (i,str(xi)+' '+str(ly)+' '+str(xi+1)+' 1 -1 0\n')
        i += 1
      # add new values: tprime
      for xi in xrange(1,lx-1):
        for yi in xrange(1,ly+1):
          para.insert (i,str(xi)+' '+str(yi)+' '+str(xi+2)+' '+str(yi)+' '+str(tp)+' 0\n')
          i += 1
      for xi in xrange(1,lx+1):
        for yi in xrange(1,ly+1):
          yup = yi+1
          if yup > ly:
            yup = 1
            ttp = -tp
          else: ttp = tp
          para.insert (i,str(xi)+' '+str(yi)+' '+str(xi)+' '+str(yup)+' '+str(ttp)+' 0\n')
          i += 1
    # sweeps
    elif '\tsweeps' in para[i]:
      # delete current values
      i += 3
      while '}' not in para[i]: del para[i]
      # add new values
      for mi in mtable:
        para.insert (i,mi+'\n')
        i += 1
    # newodrder
    if 'neworder' in para[i]:
      if zsweep:
        para[i] = '    neworder\n'
        # delete current values
        i += 3
        while '}' not in para[i]: del para[i]
        # add new values
        for xi in range (1,lx,2):
          for yi in range (1,ly+1):
            para.insert (i,'\t'+str(xi)+'  '+str(yi)+'\n')
            i += 1
            para.insert (i,'\t'+str(xi+1)+'  '+str(yi)+'\n')
            i += 1
      else:
        para[i] = '    neworderX\n'

    i += 1
  return para

def write (name,dat):
  f = open(name, 'w')
  for di in dat: f.write(di)
  f.close()

para = setval(lx=lx, ly=ly, tx=tx, ty=ty, U=U, J=J, V=V, Sz=Sz, N=N, firstmainsweep=firstmainsweep, numsweeps=numsweeps, mtable=mtable, para=base)
ofname = 'huben'+str(lx)+'x'+str(ly)+'.U'+str(U).rstrip('0').rstrip('.')+'.n'+str(n)+'.tp'+str(tp)+'.phase.in'
#ofname = 'huben'+str(lx)+'x'+str(ly)+'.U'+str(U).rstrip('0').rstrip('.')+'.N'+str(N)+'.tp0.in'
if edgeh == 1: ofname = ofname[:-2]+'edgeh.in'
elif edgeh == 2: ofname = ofname[:-2]+'edgeh2.in'
if zsweep: ofname = ofname[:-2]+'zsweep.in'
write (ofname,para)

import sys
sys.path.append('/home/chiamic/mypy')
import numpy as np
from qninput import specialqns
import setinput_localmuh as muhpy
import setinput_delta as delpy
import readinput as read
import setinput_bonds as setbnd
import setinput_mea_cdagc as meacc
import setinput_holes as sethole
import random

lx = 4#int(sys.argv[1])
ly = 4
tx = 1.0
ty = 1.0
tp = -0.32
tpp = 0
U = 8.0
J = 0.0
V = 0.0
Sz = 0
mu = 1.6
#n = 0.8435
gc = 1
yperiodic = 1

holes = lx*ly*5/32#int(float(sys.argv[2])*lx)
if gc: holes = lx*ly

# holeloc could be 0 or [[x1,y1],[x2,y2],...]
def hori_hole_loc (lx,ly,holes):
  holeloc = []
  ibeg = 1+(lx-holes)/2
  for i in xrange(ibeg,ibeg+holes):
    holeloc.append ([i,ly/2])
    print i,ly/2
  return holeloc

xx = []
def tmp_hole_loc (lx,ly):
  nstripe, ncomb = 1,0
  Nst = 10
  loc = []
  xi = 3
  while True:
    if nstripe not in [3]: yy = [1,2,4,5]
    else: yy = [1,2,3,4,5,6]
    if nstripe in [1,4]: xnext = xi + 5
    else: xnext = xi + 7
    if nstripe == 4:
      nstripe = 0
      ncomb += 1
    print xi,len(yy)
    xx.append(xi)
    for yi in yy: loc.append ([xi,yi])
    if ncomb == Nst:
      lx = xi + 2
      break
    nstripe += 1
    xi = xnext
  return loc,lx
def rand_hole_loc (lx,ly):
  loc = []
  while len(loc) < holes:
    li = [random.randint(1,lx), random.randint(1,ly)]
    if li not in loc: loc.append (li)
  return loc

holeloc=0
if gc:
    holes = 0
    #holeloc = sethole.stripe_holes (xs=[1,2,3,4,5,6],ys=[5,12])
    #holes = len(holeloc)
#else:
    #holeloc,lx = tmp_hole_loc(lx,ly)
    #holeloc = rand_hole_loc (lx,ly)
    #holeloc = sethole.stripe_holes (xs=[5,13,21,29,37,45],ys=[1,2,3,4])
    #holes = len(holeloc)
    #print 'hole number =',holes

#holeloc = hori_hole_loc (lx,ly,holes)
holeloc = 0
if holeloc != 0:
  if len(holeloc) != holes:
    print 'number of holes not match'
    print len(holeloc), holes
    exit()
  qninit = specialqns (lx,ly,holes,holeloc)
N = lx*ly-holes
n = N/float(lx*ly)

if gc: nname = 'mu'+str(mu)
else: nname = 'n'+str(n)[:7]

firstmainsweep = 0

dwx = [xx[i] for i in range(0,len(xx),2)]
def setlocalmuh (para):
  return para,''
  #muht,suft = [],''
  #muh, suffix = column_mu (ly,x=mu)
  #muh, suffix = muhpy.uniform_mu (lx,ly,mu=1.5)
  #muh, suffix = muhpy.hori_muh (lx,ly,muhset={1:[2.,0.,'mainsweeps']})
  #muht += muh
  #suft += suffix
  #muh, suffix = muhpy.hori_muh (lx,ly,muhset={1:[0,0.25,'permanent'],ly:[0,0.25,'permanent']})
  #muh, suffix = muhpy.horizontal_hole (lx,ly,holeys=[3],domain_wall=3,mu=-1.9,h=0.5,mode='warmup')
  #muht += muh
  #suft += suffix
  #muh = muht
  #muh, suffix = muhpy.linear_mu (lx,ly,mu1=1.56,mu2=2, mode='permanent')
  #field = 0.2
  #muh, suffix = muhpy.cos_hor_field (lx,ly, yc=5,mu=-field,h=0.5*field, mode='permanent')
  #muh, suffix = muhpy.stripe_muh_diag (lx,ly,holexs=xx,domain_walls=xx,h=0.5,edgeh=False)
  #muh, suffix = muhpy.hori_stripe_diag (lx,ly,xx,yy,domain=yy,h=0.25)
  #muh,suffix = muhpy.edgeh (lx,ly,hl=0.25,hr=0)
  muh,suffix = muhpy.random_muh (lx,ly,mumin=1.75,mumax=1.75,hmin=0.,hmax=2.,mode=0)
  #muh, suffix = muhpy.sinx2_mu (lx,ly,n=6,mumax=1.0,mode='permanent')
  #muh, suffix = muhpy.stripe_muh (lx,ly,holexs=[3,9,15,21,27,33,39,45],dwalls=[3,9,15,21,27,33,39,45],h=0.25,mu=[-3,-5,-3,-5,-3,-5,-3,-5],edgeh=False)
  #suffix += "24h"
  #muh,suffix = muhpy.uniform_AF (lx,ly,h=0.25,mode='warmup')
  #muh, suffix = muhpy.block_mu (lx,ly,[[1.68,1,8],[1.78,9,16],[1.68,17,24],[1.78,25,32]],mode='permanent')
  para = muhpy.setlocalmuh (para, muh)
  #print suffix
  return para, '.'+suffix

def setdelta (para):
  #return para,''
  #dels, suffix = delpy.delta_edges (lx,ly,delta=0.25,x=1,oneedge=True,yperiodic=yperiodic,xedge=False)
  #delta = 0.01
  dels,suffix = delpy.delta_all (lx,ly,delta=6,ypbc=yperiodic)
  #dels,suffix = delpy.delta_block (lx,ly,x1=1,x2=24,delta=2.,ypbc=yperiodic)
  #dels = [[1,3,1,4,0.25]]
  para = delpy.setdel (para,dels)
  return para, '.'+suffix

def setbonds (para):
  #return para,''
  #bonds,suffix = setbnd.shifted_periodic (lx,ly)
  #bonds,suffix = setbnd.diag_latt (lx,ly,pbc=False)
  bonds,suffix = setbnd.tprime (lx,ly,tp=tp,pbc=yperiodic)
  #bonds2,suffix2 = setbnd.tpprime (lx,ly,tpp=tpp,pbc=yperiodic)
  #bonds = bonds1+bonds2
  #suffix = suffix1+'.'+suffix2
  para = setbnd.setbonds (para,bonds)
  print suffix
  return para, '.'+suffix

def setmeacdagc (para):
  return para
  pairs = meacc.general (lx,ly)
  para = meacc.setpairs (para,pairs)
  return para

cdagc = 0
SplusSminus = 0
mtable = [
#	    maxstates minstates	numstr	target  noise   eps	maxiter dim	trim
'	    64		64	64	1e-10	0.0	1e-4	1	10	0',
'	    128		128	128	1e-10	0.0	1e-6	1	8	0',
'	    200		200	200	1e-12	0.0	1e-4	1	7	0',
'           200         200     200     1e-12   0.0     1e-4    1       7       0',
'           200         200     200     1e-12   0.0     1e-4    1       7       0',
'           200         200     200     1e-12   0.0     1e-4    1       7       0'
]
'''
'	    300		300	300	1e-12	0.0	1e-4	1	6	0',
'	    300		300	300	1e-12	0.0	1e-4	1	6	0',
'	    500		500	500	1e-12	0.0	1e-4	1	5	0',
'	    500		500	500	1e-12	0.0	1e-4	1	5	0',
'           800         800     800     1e-12   0.0     1e-4    1       5       0',
'           800         800     800     1e-12   0.0     1e-4    1       5       0',
'	    1400	1400	1400	1e-12	0.0	1e-4	1	4	0',
'           1400        1400    1400    1e-12   0.0     1e-4    1       4       0',
'           2400        2400    2400    1e-12   0.0     1e-4    1       4       0',
'           2400        2400    2400    1e-12   0.0     1e-4    1       4       0',
'           3000        3000    3000    1e-12   0.0     1e-4    1       4       0',
'           3000        3000    3000    1e-12   0.0     1e-4    1       4       0',
'           4000        4000    4000    1e-12   0.0     1e-4    1       4       0',
'           4000        4000    4000    1e-12   0.0     1e-4    1       4       0',
'           5000        5000    5000    1e-12   0.0     1e-4    1       4       0',
'           5000        5000    5000    1e-12   0.0     1e-4    1       4       0',
'           6000        6000    6000    1e-12   0.0     1e-4    1       4       0',
'           6000        6000    6000    1e-12   0.0     1e-4    1       4       0',
'           7000        7000    7000    1e-12   0.0     1e-4    1       4       0',
'           7000        7000    7000    1e-12   0.0     1e-4    1       4       0',
'           8000        8000    8000    1e-12   0.0     1e-4    1       4       0',
'           8000        8000    8000    1e-12   0.0     1e-4    1       4       0',
'           9000        9000    9000    1e-12   0.0     1e-4    1       4       0',
'           9000        9000    9000    1e-12   0.0     1e-4    1       4       0',
#'           9000        9000    9000    1e-12   0.0     1e-4    1       4       0',
#'           9000        9000    9000    1e-12   0.0     1e-4    1       4       0',
#'           10000       10000   10000    1e-12   0.0     1e-4    1       4       0',
#'           10000       10000   10000    1e-12   0.0     1e-4    1       4       0',
#'	    11000	11000	11000	1e-12	0.0	1e-4	1	3	0',
#'	    11000	11000	11000	1e-12	0.0	1e-4	1	3	0',
'           12000       12000   12000   1e-12   0.0     1e-4    1       3       0',
'           12000       12000   12000   1e-12   0.0     1e-4    1       3       0',
#'           13000       13000   13000   1e-12   0.0     1e-4    1       3       0',
#'           13000       13000   13000   1e-12   0.0     1e-4    1       3       0',
#'           15000       15000   15000   1e-12   0.0     1e-4    1       3       0',
#'           15000       15000   15000   1e-12   0.0     1e-4    1       3       0',
#'           17000       17000   17000   1e-12   0.0     1e-4    1       3       0',
#'           17000       17000   17000   1e-12   0.0     1e-4    1       3       0',
#'           20000       20000   20000   1e-12   0.0     1e-4    1       3       0',
#'           20000       20000   20000   1e-12   0.0     1e-4    1       3       0',
#'           23000       23000   23000   1e-12   0.0     1e-4    1       3       0',
#'           23000       23000   23000   1e-12   0.0     1e-4    1       3       0',
#'           26000       26000   26000   1e-12   0.0     1e-4    1       3       0',
#'           26000       26000   26000   1e-12   0.0     1e-4    1       3       0',
#'           30000       30000   30000   1e-12   0.0     1e-4    1       3       0',
#'           30000       30000   30000   1e-12   0.0     1e-4    1       3       0',
#'           35000       35000   35000   1e-12   0.0     1e-4    1       3       0',
#'           35000       35000   35000   1e-12   0.0     1e-4    1       3       0',
#'           40000       40000   40000   1e-12   0.0     1e-4    1       3       0',
#'           40000       40000   40000   1e-12   0.0     1e-4    1       3       0',
]'''
if type(N) != int:
  if not  N.is_integer():
    print 'Error: N is not an integer'
    exit()
N = int(N)
if n.is_integer(): n = int(n)
numsweeps = len(mtable)
base = '/home/chiamin/mypy/dmrg/para/huben.sample'
base = list(open(base))

def setval (lx,ly,tx,ty,U,J,V,Sz,N,numsweeps,mtable,para):
  i = 0
  while i < len(para):
    if 'lx =' in para[i]: para[i] = '\tlx = '+str(lx)+'\n'
    elif 'ly =' in para[i]: para[i] = '\tly = '+str(ly)+'\n'
    elif 'tx =' in para[i]: para[i] = '    tx = '+str(tx)+'\n'
    elif 'ty =' in para[i]: para[i] = '    ty = '+str(ty)+'\n'
    elif 'U =' in para[i]: para[i] = '    U = '+str(U)+'\n'
    elif 'J =' in para[i]: para[i] = '    J = '+str(J)+'\n'
    elif 'V =' in para[i]: para[i] = '    V = '+str(V)+'\n'
    elif 'mu =' in para[i]: para[i] = '    mu = '+str(mu)+'\n'
    elif 'periodic =' in para[i]: para[i] = '        periodic = '+str(yperiodic)+'\n'
    elif 'Sz =' in para[i]: para[i] = '\tSz = '+str(Sz)+'\n'
    elif 'Nf =' in para[i]:
      if mu == 0: para[i] = '\tNf = '+str(N)+'\n'
      else: para[i] = '\tNf = 0\n'
    elif 'firstmainsweep =' in para[i]: para[i] = '\tfirstmainsweep = '+str(firstmainsweep)+'\n'
    elif 'numsweeps =' in para[i]: para[i] = '\tnumsweeps = '+str(numsweeps)+'\n'
    # localfields
    elif 'localfields' in para[i]: para[i] = '    localfieldsX\n'
    # localmuh
    elif 'localmuh' in para[i]: para[i] = '    localmuhX\n'
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
  print name
  f = open(name, 'w')
  for di in dat: f.write(di)
  f.close()

para = setval(lx=lx, ly=ly, tx=tx, ty=ty, U=U, J=J, V=V, Sz=Sz, N=N, numsweeps=numsweeps, mtable=mtable, para=base)
para, suffix = setlocalmuh (para)
para, suffixdel = setdelta (para)
para, suffixbnd = setbonds (para)
para = setmeacdagc (para)
suffixtx = ''
if tx != 1.: suffixtx = '.tx'+str(tx)
ofname = 'huben'+str(lx)+'x'+str(ly)+suffixtx+'.U'+str(U).rstrip('0').rstrip('.')+'.'+nname+suffixbnd+suffix+suffixdel+'.in'
write (ofname,para)

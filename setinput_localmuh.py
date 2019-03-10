import sys
sys.path.append('/home/chiamic/mypy')
import numpy as np
from qninput import specialqns
from math import pi, sin
import random
#parafile = sys.argv[1]

def main():
  parafile = sys.argv[1]
  para = list(open(parafile))
  lx,ly = readlxly (para)
  muh, suffix = horizontal_hole (lx,ly, holey=(ly+1)/2)
  para = setlocalmuh (para, muh, firstsweep=8)
  write (parafile, para, suffix)


#----------- define muh patterns -----------

def column_mu (ly,x,mu):
  muh = []
  mode = 2 # permanent
  for y in xrange(1,ly+1):
      hi = 0
      mui = mu
      muh.append ([x,y,mode,mui,hi])
  return muh,'columnmu'

def uniform_mu (lx,ly,mu):
  muh = []
  mode = 0 # first few sweeps
  for x in xrange(1,lx+1):
    for y in xrange(1,ly+1):
      hi = 0
      mui = mu
      muh.append ([x,y,mode,mui,hi])
  return muh,'uniformmu'

def random_muh (lx,ly,mumin,mumax,hmin,hmax,mode=0):
  muh = []
  for x in xrange(1,lx+1):
    for y in xrange(1,ly+1):
      hi = random.uniform (hmin,hmax)
      mui = random.uniform (mumin,mumax)
      muh.append ([x,y,mode,mui,hi])
  suf = ''
  if mumin != mumax: suf +='randmu_'+str(mumin)+'_'+str(mumax)
  if hmin != hmax: suf += 'randh_'+str(hmin)+'_'+str(hmax)
  return muh,suf

def random_loc_mu (lx,ly,mu,N,mode=0):
  muh,xy = [],[]
  while N > 0:
    x = random.randint (1,lx)
    y = random.randint (1,ly)
    if [x,y] not in xy:
      xy.append ([x,y])
      N -= 1
  for x,y in xy:
      muh.append ([x,y,mode,mu,0.])
  return muh,'randloc'+str(N)+'_mu'+str(mu)

def edgeh (lx,ly,hl,hr):
  hl *= 0.5
  hr *= 0.5
  muh = []
  mode = 2 # permanant
  for x in [1,lx]:
    for y in xrange(1,ly+1):
      hi = (-1)**y*0.5
      if x == 1: hi = hi*hl
      else: hi = hi*hr
      muh.append ([x,y,mode,0,hi])
  return muh,'edgeh'

def uniform_AF (lx,ly,h,mode='permanent'):
  h *= 0.5
  mode = get_mode (mode)
  muh = []
  for x in xrange(1,lx+1):
    for y in xrange(1,ly+1):
      hi = h * (-1)**(x % 2 == y % 2)
      mui = 0.
      muh.append ([x,y,mode,mui,hi])
  return muh,'AF'

def block_mu (lx,ly,mu_x1_x2s,mode='permanent'):
# mu_x1_x2s = [[mu,x1,x2],...], where set mu between x1 and x2 for all y
  mode = get_mode (mode)
  muh = []
  suf = ''
  for mu,x1,x2 in mu_x1_x2s:
    suf += '_'+str(mu)
    for x in xrange(1,lx+1):
      for y in xrange(1,ly+1):
        if x >= x1 and x <= x2:
          muh.append ([x,y,mode,mu,0.])
  return muh,'blockmu'+suf

def hori_muh (lx,ly,muhset):
# muhset={y1:[mu1,h1,mode1],...}
  muh = []
  for y in xrange(1,ly+1):
    for x in xrange(1,lx+1):
      if y in muhset:
        hi = (-1)**x*muhset[y][1]*0.5
        mui = muhset[y][0]
        mode = get_mode (muhset[y][2])
        muh.append ([x,y,mode,mui,hi])
  return muh, 'horimuh'

def stripe_muh (lx,ly,holexs,dwalls,h,mu,edgeh=False):
  h *= 0.5
  if type(mu) == float:
    mutmp = mu
    mu = [mutmp for i in xrange(len(holexs))]
  elif type(mu) != list:
    raise Exception
  muh = []
  idomain = 0
  hsign = 1.
  for x in xrange(1,lx+1):
    for y in xrange(1,ly+1):
      if x in holexs:
        ind = holexs.index(x)
        mui = mu[ind]
        hi = 0.
      else:
        if idomain < len(dwalls) and x > dwalls[idomain]:
           hsign *= -1.
           idomain += 1
        mui = 0.
        hi = hsign * h * (-1)**(x % 2 == y % 2)
      if edgeh and (x==1 or x==lx):
        mode = 2 # permanent
      else:
        mode = 0 # warm up
      muh.append ([x,y,mode,mui,hi])
  if edgeh: suffix = 'pattern.edgeh'
  else: suffix = 'pattern'
  return muh, suffix

def stripe_muh_diag (lx,ly,holexs,domain_walls,h,edgeh=False):
  h *= 0.5
  muh = []
  idomain = 0
  hsign = 1.
  for x in xrange(1,lx+1):
    for y in xrange(1,ly+1):
      if x in holexs:
        mui = -2.
        hi = 0.
      else:
        if idomain < len(domain_walls) and x > domain_walls[idomain]:
           hsign *= -1.
           idomain += 1
        mui = 0.
        hi = hsign * h * (-1)**(x % 2)
      if edgeh and (x==1 or x==lx):
        mode = 2 # permanent
      else:
        mode = 0 # warm up
      muh.append ([x,y,mode,mui,hi])
  if edgeh: suffix = 'pattern.edgeh'
  else: suffix = 'pattern'
  return muh, suffix

def hori_stripe_diag (lx,ly,holex,holey,domain,h):
  h *= 0.5
  muh = []
  idomain = 0
  hsign = 1.
  for y in xrange(1,ly+1):
    for x in xrange(1,lx+1):
      if x in holex and y in holey:
        mui,hi = -2.,0.
      else:
        if idomain < len(domain) and y > domain[idomain]:
          hsign *= -1
          idomain += 1
        mui = 0.
        hi = hsign * h * (-1)**(x % 2)
      mode = 0 # warm up
      muh.append ([x,y,mode,mui,hi])
  suffix = 'hori'
  return muh, suffix

def linear_mu (lx,ly,mu1,mu2,mode):
  mode = get_mode (mode)
  muh = []
  dmu = float(mu2 - mu1)/float(lx-1)
  for y in xrange(1,ly+1):
    for x in xrange(1,lx+1):
      mui = mu1 + (x-1)*dmu
      hi = 0.
      muh.append ([x,y,mode,mui,hi])
  return muh, 'mu'+str(mu1)+'_'+str(mu2)

def sinx2_mu (lx,ly,n,mumax,mode='permanent'):
  mode = get_mode (mode)
  muh = []
  for x in xrange(1,lx+1):
    mui = -mumax * (sin(n*pi*(x-1)/(lx-1)))**2
    for y in xrange(1,ly+1):
      muh.append ([x,y,mode,mui,0.])
  return muh, 'sinx2'

def cosy_field (lx,ly,yc,mu=-0.1,h=0.05,mode='permanent'):
  mode = get_mode (mode)
  muh = []
  for y in xrange(1,ly+1):
    mui = mu * np.cos((y-yc)*pi/float(ly))
    for x in xrange(1,lx+1):
      if y == 1:
        hi = h * (-1)**(x % 2 == y % 2)
      elif y == ly:
        hi = -h * (-1)**(x % 2 == y % 2)
      else:
        hi = 0.
      muh.append ([x,y,mode,mui,hi])
  return muh, 'cosfield'

def horizontal_hole (lx,ly,holeys,domain_wall,mu=-2,h=0.5,mode='warmup'):
  h *= 0.5
  mode = get_mode (mode)
  muh = []
  for y in xrange(1,ly+1):
    for x in xrange(1,lx+1):
      if y in holeys:
        muh.append ([x,y,mode,mu,0])
      elif y < domain_wall:
        sign = (-1)**(x % 2 == y % 2)
        muh.append ([x,y,mode,0,sign*h])
      else:
        sign = -1 * (-1)**(x % 2 == y % 2)
        muh.append ([x,y,mode,0,sign*h])
  return muh, 'horpattern'

#--------- end of muh pattern ------------

def get_mode (mode):
  if mode == 'permanent':
    return 2
  elif mode == 'warmup':
    return 0
  elif mode == 'mainsweeps':
    return 1
  else:
    print 'Invalid mode:',mode
    raise

def readlxly (para):
  i = 0
  while i < len(para):
    if 'lx =' in para[i]:
        temp = para[i].split()
        lx = int(temp[-1])
    elif 'ly =' in para[i]:
        temp = para[i].split()
        ly = int(temp[-1])
        return lx, ly

def setlocalmuh (para,muh,firstsweep=-1):
  if muh == []: return para

  i = 0
  while i < len(para):
    if firstsweep > 0 and 'firstmainsweep =' in para[i]:
        para[i] = '\tfirstmainsweep = '+str(firstsweep)+'\n'
    if 'localmuh' in para[i]:
        para[i] = '    localmuh\n'
        # store index of 'numsite'
        while 'numsite' not in para[i]: i += 1
        para[i] = '        numsite = '+str(len(muh))+'\n'
        # delete current values
        while 'sites' not in para[i]: i += 1
        i += 3
        while '}' not in para[i]: del para[i]
        # add new values
        for muhi in muh:
            xi,yi,mode,mui,hi = muhi[0],muhi[1],muhi[2],muhi[3],muhi[4]
            para.insert (i,'            '+str(xi)+'   '+str(yi)+'       '+str(mode)+'       '+str(mui)+'       '+str(hi)+'\n')
            i += 1
    i += 1
  return para

def write (name,dat,suffix=''):
  if suffix not in name:
    name = name[:-2]+suffix+'.in'
  f = open(name, 'w')
  for di in dat: f.write(di)
  f.close()

#main()

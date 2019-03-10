def diag_latt (lx,ly,pbc=1):
  bonds = []
  for xi in xrange(1,lx,2):
    for yi in xrange(2,ly+1):
      bonds.append ([xi,yi,xi+1,yi-1,1])
    if pbc:
      bonds.append ([xi,1,xi+1,ly,1])
  for xi in xrange(2,lx,2):
    for yi in xrange(1,ly):
      bonds.append ([xi,yi,xi+1,yi+1,1])
    if pbc:
      bonds.append ([xi,ly,xi+1,1,1])
  return bonds,'diag'

def shifted_periodic (lx,ly):
  t = 1
  re = [] # return [x1,y1,x2,y2,t]
  for x1 in xrange(1,lx):
    re.append ([x1,1,x1+1,ly,t])
  return re, 'spiral'

def tprime (lx,ly,tp,pbc=True):
  if tp == 0:
    return [],''
  re = []
  for x in range(1,lx+1):
    for y in range(1,ly+1):
      xp = x+1
      xm = x-1
      yp = y+1
      if yp <= ly or pbc:
        if yp > ly: yp = 1
        if xm >= 1:
          re.append ([x,y,xm,yp,tp])
        if xp <= lx:
          re.append ([x,y,xp,yp,tp])
  return re,'tp'+str(tp)

def tpprime (lx,ly,tpp,pbc=True):
  if tpp == 0: return [],''
  re = []
  for x in xrange(1,lx+1):
    for y in xrange(1,ly+1):
      xp = x+2
      yp = y+2
      if yp <= ly or pbc:
        if yp > ly: yp -= ly
        re.append ([x,y,x,yp,tpp])
      if xp <= lx:
        re.append ([x,y,xp,y,tpp])
  return re,'tpp'+str(tpp)

'''
    extrabondsX
        {
        numbonds = 15
        bonds
            {
            x1 y1      x2      y2      tval     jval
            }
        }
'''
def setbonds (para,bonds):
  if bonds == []: return para

  i = 0
  while i < len(para):
    if 'extrabonds' in para[i]:
        para[i] = '    extrabonds\n'
        # store index of 'numsite'
        while 'numbonds' not in para[i]: i += 1
        para[i] = '        numbonds = '+str(len(bonds))+'\n'
        # delete current values
        while ' bonds' not in para[i]: i += 1
        i += 3
        while '}' not in para[i]: del para[i]
        # add new values
        for bi in bonds:
            x1,y1,x2,y2,t = bi
            para.insert (i,'            '+str(x1)+'  '+str(y1)+'  '+str(x2)+'  '+str(y2)+'  '+str(t)+'  0\n')
            i += 1
    i += 1
  return para

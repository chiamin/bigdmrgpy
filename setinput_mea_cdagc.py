def general (lx,ly):
  pairs=[]
  for x1 in xrange(1,lx+1):
    for y1 in xrange(1,ly+1):
      for x2 in xrange(1,lx+1):
        for y2 in xrange(1,ly+1):
          if [x2,y2,x1,y1] not in pairs:
            pairs.append ([x1,y1,x2,y2])
  return pairs

#---------------------------------------------------
def setpairs (para,pairs):
  if pairs == []: return para

  i = 0
  while i < len(para):
    if 'docdagc' in para[i]:
        para[i] = '    docdagc\n'
        # set the mode
        while 'standard' not in para[i]: i += 1
        para[i] = '        standard = no\n'
        while 'manypairs' not in para[i]: i += 1
        para[i] = '        manypairs = yes\n'
        while 'allpairs' not in para[i]: i += 1
        para[i] = '        allpairs = no\n'
        # set the number of pairs
        while 'numpairs' not in para[i]: i += 1
        para[i] = '        numpairs = '+str(len(pairs))+'\n'
        # delete current values
        while ' pairs' not in para[i]: i += 1
        i += 3
        while '}' not in para[i]: del para[i]
        # add new values
        for pi in pairs:
            x1,y1,x2,y2 = pi
            para.insert (i,'           '+str(x1)+'   '+str(y1)+'       '+str(x2)+'       '+str(y2)+'\n')
            i += 1
    i += 1
  return para

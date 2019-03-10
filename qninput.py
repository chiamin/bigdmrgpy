
def specialqns (nx,ny,nh,loc,nrest=3):
  # loc is the holes location = [[x1,y1],[x2,y2],...]
  holex = ['']
  holey = ['']
  for loci in loc:
    holex.append (loci[0])
    holey.append (loci[1])

  #for i in xrange(1,nh+1):
  #  print holex[i], holey[i]

  lastqn = 1

  if holex[1] == 1 and holey[1] == 1:
    lastqn = 0

  rr = []
  for i in range(1,nx*ny+1):
    x = int(i/ny)+1
    y = i-(x-1)*ny+1
    lenn = i+1+nrest
    if lenn % 2 == 1: lenn -= 1
    if lenn > nx*ny: lenn -= 2
    if lenn > nx*ny: lenn -= 2
    if lenn > nx*ny: lenn -= 2
    nr = lenn-i-1
    holehere = 0
    for j in range(1,nh+1):
      if holex[j] == x and holey[j] == y: holehere = 1
    if holehere == 0:
      qn = lastqn + 1 + nr
      lastqn += 1
    else:
      qn = lastqn
    #print i, qn%2, qn
    rr.append (str(i)+' '+str(qn%2)+' '+str(qn))
  return rr
#specialqns (3,3,2,[[1,1],[1,2]])

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
    i += 1

def read_periodic (para):
  i = 0
  while i < len(para):
    if 'periodic = ' in para[i]:
      temp = para[i].split()
      periodic = int(temp[-1])
      return periodic
    i += 1

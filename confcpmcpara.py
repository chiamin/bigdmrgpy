import sys

def readpara (fname):
  f = open (fname)
  return f.readlines()

def writepara (fname, para):
  f = open (fname,'w')
  for line in para:
    f.write (line)
  f.close()

def setpara (para, name, val):
  for i in xrange(len(para)):
    if name in para[i]:
      loc = para[i].find('=')
      para[i] = para[i][:loc+1] + ' ' + str(val) + '\n'
      return para;
  print name,'not found'
  exit()



#para = readpara (sys.argv[1])
#para = setpara (para, 'Lx', 8)
#writepara ('test',para)

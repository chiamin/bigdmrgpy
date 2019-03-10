import sys, os
from random import randint

base = sys.argv[1]
Ninput = int(sys.argv[2])
Nfrom = 1
if len(sys.argv) > 3:
  Nfrom = int(sys.argv[3]) 
f = open (base,'r')
dat = [line for line in f]
f.close()

def set_para (dat, name, val):
  search = name + ' = '
  for i in range(len(dat)):
    loc = dat[i].find (search)
    if loc != -1:
      dat[i] = dat[i][:loc + len(search)] + str(val) + '\n'
      return dat
  print ('parameter not found: '+name)
  return dat

for n in xrange(Nfrom,Nfrom+Ninput):
  par = set_para (dat,'rseed',randint(100000000,999999999))

  outfile = base+'_'+str(n)+'.in'
  f = open (outfile, 'w')
  for line in dat: f.write (line)
  f.close()

  print outfile

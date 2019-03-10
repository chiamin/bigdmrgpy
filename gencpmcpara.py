from random import randint
import sys, os
sys.path.append('/home/chiamic/mypy')
from confcpmcpara import *

N = sys.argv[1]
if '-' in N:
  temp = N.split('-')
  Nbeg,Nend = int(temp[0]),int(temp[1])
  print Nbeg
  print Nend
else:
  Nbeg,Nend = 1,int(N)
basepara = sys.argv[2]
name = sys.argv[3]
paradir = sys.argv[4]

if not os.path.exists (paradir):
  os.makedirs (paradir)
#elif not os.listdir (paradir) == []:
#  os.system ('rm '+paradir+'/*')

para = readpara (basepara)
for i in xrange(Nbeg,Nend+1):
  seed = randint (100000000,999999999)
  para = setpara (para,'rseed',seed)
  writepara (paradir+'/'+name+'.cp'+str(i)+'.in',para)

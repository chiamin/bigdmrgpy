import sys, os
from random import randint

base = sys.argv[1]
output = sys.argv[2]

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

def replace_para (dat, fr, to):
  for i in range(len(dat)):
    if fr in dat[i]:
      dat[i] = dat[i].replace (fr, to)
  return dat

def get_para (dat, name):
  search = name + ' = '
  for line in dat:
    loc = line.find (search)
    if loc != -1:
      return line[loc+len(search):].rstrip('\n')
  print ('parameter not found: '+name)

# Set parameters
#dat = set_para (dat, 'GMPS_block_size', arg)
dat = set_para (dat, 'rseed', randint(100,1000000000))

jobname = output.rstrip('.in')
bkdir = os.getcwd()+'/backup/'
dat = set_para (dat, 'cpmc_file', bkdir+jobname+'.cpmc')

bkdir = os.getcwd() + '/backup/'
try: os.mkdir (bkdir)
except OSError: pass
dat = replace_para (dat, '$backup_dir', bkdir)
jobname = output.rstrip('.in')
dat = replace_para (dat, '$jobname', jobname)



f = open (output, 'w')
for line in dat: f.write (line)
f.close()

#!/usr/bin/python

import serial,os
cmd = os.system
for i in range(3):
    try: ser = serial.Serial('/dev/ttyUSB%d'%i, 115200)
    except Exception as e:
        if i == 2: raise e
    else: break
print 'Connected to', ser.name
MODEL = 0

CMDS = {
168 : ('RANDOM', 'awsetbg -r /home/adrian/Wallpaper/DesktopPhotos'),
80 : ('VOL DOWN', 'amixer -q sset Master 3%-'),
208 : ('VOL UP', 'amixer -q sset Master 3%+'),
112 : ('SLEEP', 'sudo pm-suspend')
}

def int2ss(ss):
    return ''.join((str(th),chr(th+ord('a')-10))[th > 9] for th in ss)
def valid(ss):
    return sorted((th+i)%len(ss) for i,th in enumerate(ss)) == range(len(ss))
def disp():
    print int2ss(ss), '-', ('Invalid','Valid')[valid(ss)]
def add10():
    if ss and ss[-1] < 26: ss[-1] += 10
def simulate():
    if valid(ss) and ss:
        cmd('google-chrome jugglinglab.sourceforge.net/siteswap.php?'+int2ss(ss))
    clear()
def clear():
    global ss
    ss = []
def restart():
    cmd('python ~/IRserial.py')
    exit()

FUNCTIONS = {
200 : ('MEM/DISP - show SS', disp),
178 : ('+10', add10),
176 : ('X-BASS - clear', clear),
48 : ('EQUALIZER - simulate', simulate),
72 : ('REPEAT - restart script', restart),
0 : ('POWER - exit', exit)
}

NUMBERS = {
146 : 0,
2 : 1,
34 : 2,
18 : 3,
50 : 4,
10 : 5,
42 : 6,
26 : 7,
130 : 8,
162 : 9
}

ss = []

while 1:
  try:
    inp = ser.readline().strip()
    m,v = map(int,inp.split())
  except Exception:
    print inp
  else:
    if m == MODEL:
      if v in NUMBERS:
        ss.append(NUMBERS[v])
        print NUMBERS[v]
      elif v in CMDS:
        cmd(CMDS[v][1])
        print CMDS[v][0]
      elif v in FUNCTIONS:
        FUNCTIONS[v][1]()
        print FUNCTIONS[v][0]
      else:
        print v
        


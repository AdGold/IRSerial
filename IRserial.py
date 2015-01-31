#!/usr/bin/python

import serial,os
import media

cmd = os.system
for i in range(3):
    try: ser = serial.Serial('/dev/ttyUSB%d'%i, 115200)
    except Exception as e:
        if i == 2: raise e
    else: break
print('Connected to', ser.name)
MODEL = 0

CMDS = {
168 : ('RANDOM', 'awsetbg -r /home/adrian/Wallpaper/DesktopPhotos'),
112 : ('SLEEP', 'sudo pm-suspend')
}

def restart():
    cmd('python ~/scripts/IRSerial/IRserial.py')
    exit()

FUNCTIONS = {
176 : ('X-BASS - restart sccript',  restart),
0   : ('POWER - exit',              exit),
32  : ('CD - Play/Pause',           lambda:media.send('PlayPause')),
40  : ('USB - Play/Pause',          lambda:media.send('PlayPause')),
144 : ('<< - Previous track',       lambda:media.send('Prev')),
192 : ('>> - Next track',           lambda:media.send('Next')),
16  : ('STOP - Stop',               lambda:media.send('Stop')),
72  : ('REPEAT - toggle repeat',    lambda:media.send('Repeat')),
80 : ('VOL DOWN',                   lambda:media.send('down', 'beep')),
208 : ('VOL UP',                    lambda:media.send('up', 'beep')),
}

while 1:
  try:
    inp = ser.readline().strip()
    m,v = list(map(int,inp.split()))
  except Exception:
    print(inp)
  else:
    if m == MODEL:
      if v in CMDS:
        cmd(CMDS[v][1])
        print(CMDS[v][0])
      elif v in FUNCTIONS:
        FUNCTIONS[v][1]()
        print(FUNCTIONS[v][0])
      else:
        print(v)



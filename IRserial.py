#!/usr/bin/python

import serial
import os
from media import send as media


def restart():
    cmd('python ~/scripts/IRSerial/IRserial.py')
    exit()

COMMANDS = {
    0: {
        203: ('Restart script',   restart),
        0: ('Quit',               exit),
        209: ('Play/Pause',       lambda: media('PlayPause')),
        169: ('Previous track',   lambda: media('Prev')),
        83: ('Next track',        lambda: media('Next')),
        147: ('Stop',             lambda: media('Stop')),
        41: ('Repeat',            lambda: media('Repeat')),
        11: ('Vol Down',          lambda: media('down', 'beep')),
        139: ('Vol Up',           lambda: media('up', 'beep')),
        105: ('Mute',             lambda: media('mute')),
        163: ('Slepp',            'sudo pm-suspend'),
        75: ('Right',             'i3-msg workspace next'),
        9: ('Left',               'i3-msg workspace prev'),
    },
    6: {
        126: ('Vol Down',          lambda: media('down')),
        190: ('Vol Up',           lambda: media('up')),
    },
}

run = os.system
for i in range(3):
    try:
        ser = serial.Serial('/dev/ttyUSB%d' % i, 115200)
    except Exception as e:
        if i == 2:
            raise e
    else:
        break
print('Connected to', ser.name)

while 1:
    try:
        inp = ser.readline().strip()
        m, v = list(map(int, inp.split()))
    except Exception:
        print(inp)
    else:
        if m in COMMANDS and v in COMMANDS[m]:
            cmd = COMMANDS[m][v]
            if isinstance(cmd[1], str):
                run(cmd[1])
            else:
                cmd[1]()
            print(cmd[0])
        else:
            print('%d %d' % (m, v))

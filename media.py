#! /usr/bin/python

import os, subprocess, sys, dbus
from clementine import Clementine

vlc_pre = 'dbus-send --session --type=method_call --print-reply --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.'

vlc = {
    'playpause':'PlayPause',
    'next':'Next',
    'prev':'Previous',
    'stop':'Stop',
    'repeat':'Repeat',
}

def send(cmd, *args):
    processes = subprocess.check_output(['ps', '-e']).decode('utf-8')

    if 'clementine' in processes:
        Clementine.send(cmd.title(), *args)
    elif 'vlc' in processes:
        os.system(vlc_pre+vlc[cmd.lower()])
    else:
        pass

if __name__ == '__main__':
    send(sys.argv[1])

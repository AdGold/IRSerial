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

mplayer_fifo = '/home/adrian/.mplayerremote'
mplayer_format = 'echo "{}" > '+mplayer_fifo

mplayer = {
    'playpause':'pause', #doesn't work on a complete stop...
    'next':'pt_step 1 1', #only steps while playing video
    'prev':'pt_step -1 1', #also moves forward...
    'stop':'stop', #only part that works properly
    'repeat':'Repeat', #actually loop 0 for repeat and loop -1 
}

if not os.path.exists(mplayer_fifo):
    os.system('mkfifo '+mplayer_fifo)

def send(cmd, *args):
    processes = subprocess.check_output(['ps', '-e']).decode('utf-8')

    if 'clementine' in processes:
        Clementine.send(cmd.title(), *args)
    elif 'vlc' in processes:
        os.system(vlc_pre+vlc[cmd.lower()])
    elif 'mplayer' in processes or 'smplayer' in processes:
        os.system(mplayer_format.format(mplayer[cmd.lower()]))
    else:
        pass

if __name__ == '__main__':
    send(sys.argv[1])

#! /usr/bin/python

import os, subprocess, sys
from clementine import Clementine

vlc = {
    'playpause':'dbus-send --session --type=method_call --print-reply --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause',
    'next':'dbus-send --session --type=method_call --print-reply --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next',
    'prev':'dbus-send --session --type=method_call --print-reply --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous',
    'stop':'dbus-send --session --type=method_call --print-reply --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Stop',
}

def send(cmd):
    processes = subprocess.check_output(['ps', '-e']).decode('utf-8')

    if 'clementine' in processes:
        Clementine.send(cmd)
    elif 'vlc' in processes:
        os.system(vlc[cmd.lower()])
    else:
        pass

if __name__ == '__main__':
    send(sys.argv[1])

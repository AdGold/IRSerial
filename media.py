#! /usr/bin/python

import os, subprocess, sys, dbus, re
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

vol_step = 2
vol_timeout = 500
vol_beep = '/home/adrian/scripts/IRSerial/volume.wav'
volume_cmds = {
    'up':'amixer sset Master {}%+'.format(vol_step),
    'down':'amixer sset Master {}%-'.format(vol_step),
    'mute':'amixer sset Master toggle'
}

if not os.path.exists(mplayer_fifo):
    os.system('mkfifo '+mplayer_fifo)

def do_volume(cmd, snd):
    os.system(volume_cmds[cmd])
    detail = subprocess.check_output(['amixer', 'get', 'Master']).decode('utf-8')
    detail = [line for line in detail.split('\n') if '%]' in line][0]
    muted = 'off' in detail
    if not muted and snd:
        os.system('mplayer %s' % vol_beep)
    volume = int(re.search(r'\[(\d+)%\]', detail).group(1))
    if cmd == 'mute' and muted:
        icon = 'audio-volume-muted'
    else:
        icon = 'audio-volume-' + ('low', 'medium', 'high')[volume//34]
    blocks = volume//5
    bar = '[' + '='*blocks + '-'*(2*(20-blocks)) + ']'
    title = 'Volume: ' + (str(volume)+'%' if not muted else 'Muted')
    os.system('notify-send %r %r -i %r -t %d' % (title, bar, icon, vol_timeout))
    return volume, muted


def send(cmd, *args):
    if cmd in volume_cmds:
        do_volume(cmd, len(args) > 0 and args[0] == 'beep')
        return
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
    send(sys.argv[1], *sys.argv[2:])

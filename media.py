#! /usr/bin/python

import os
import subprocess
import sys
import re
from clementine import Clementine

vlc_pre = 'dbus-send --session --type=method_call --print-reply'\
    '--dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 '\
    'org.mpris.MediaPlayer2.Player.'

vlc = {
    'playpause': 'PlayPause',
    'next': 'Next',
    'prev': 'Previous',
    'stop': 'Stop',
    'repeat': 'Repeat',
}

mplayer_fifo = '/home/adrian/.mplayerremote'
mplayer_format = 'echo "{}" > '+mplayer_fifo

mplayer = {
    'playpause': 'pause',  # doesn't work on a complete stop...
    'next': 'pt_step 1 1',  # only steps while playing video
    'prev': 'pt_step -1 1',  # also moves forward...
    'stop': 'stop',  # only part that works properly
    'repeat': 'Repeat',  # actually loop 0 for repeat and loop -1
}

vol_step = 2
vol_timeout = 500
vol_beep = '/home/adrian/scripts/IRSerial/volume.wav'
volume_cmds = {
    'up': 'amixer -D pulse sset Master {}%+'.format(vol_step),
    'down': 'amixer -D pulse sset Master {}%-'.format(vol_step),
    'mute': 'amixer -D pulse sset Master toggle'
}

if not os.path.exists(mplayer_fifo):
    os.system('mkfifo '+mplayer_fifo)


def do_volume(cmd, snd):
    os.system(volume_cmds[cmd])
    cmd = ['amixer', '-D', 'pulse', 'get', 'Master']
    detail = subprocess.check_output(cmd).decode('utf-8')
    detail = [line for line in detail.split('\n') if '%]' in line][0]
    muted = 'off' in detail
    if not muted and snd:
        # os.system('mplayer %s' % vol_beep)
        os.system('aplay %s' % vol_beep)
    volume = int(re.search(r'\[(\d+)%\]', detail).group(1))
    if muted:
        icon = 'audio-volume-muted'
    elif volume == 0:
        icon = 'audio-volume-off'
    else:
        icon = 'audio-volume-' + ('low', 'medium', 'high')[volume//34]
    # blocks = volume//5
    # bar = '[' + '='*blocks + '-'*(2*(20-blocks)) + ']'
    # title = 'Volume: ' + (str(volume)+'%' if not muted else 'Muted')
    # os.system('notify-send %r %r -i %r -t %d' %
    # (title, bar, icon, vol_timeout))
    cmd = 'notify-send " " -i notification-%s -t %d ' \
        '-h int:value:%d -h string:synchronous:volume'
    os.system(cmd % (icon, vol_timeout, volume))

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

import dbus

class clem:
    def __init__(self):
        self.session_bus = dbus.SessionBus()
        self.player = self.session_bus.get_object('org.mpris.clementine', '/Player')
        self.iface = dbus.Interface(self.player, dbus_interface='org.freedesktop.MediaPlayer')
    def send(self, cmd, *args):
        if cmd.lower() == 'playpause':
            cmd = 'Play' if self.iface.GetStatus()[0] else 'Pause'
        self.iface.__getattr__(cmd)(*args)

Clementine = clem()

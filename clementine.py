import dbus

class clem:
    def __init__(self):
        try:
            self.session_bus = dbus.SessionBus()
            self.player = self.session_bus.get_object('org.mpris.clementine', '/Player')
            self.iface = dbus.Interface(self.player, dbus_interface='org.freedesktop.MediaPlayer')
#            self.iface.connect_to_signal('TrackChange', self.track_change)
        except dbus.exceptions.DBusException:
            self.init = False
        else:
            self.init = True
    def track_change(self, sender=None):
        print('track changed, sender =', sender)
    def send(self, cmd, *args):
        if not self.init:
            self.__init__()
        if not self.init:
            return

        if cmd.lower() == 'playpause':
            cmd = 'Play' if self.iface.GetStatus()[0] else 'Pause'
        elif cmd.lower() == 'repeat':
            args = (self.iface.GetStatus()[2] == 0,)
        print(args, cmd)
        self.iface.__getattr__(cmd)(*args)

Clementine = clem()

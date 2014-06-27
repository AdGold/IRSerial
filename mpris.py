import dbus

class mpris:
    def __init__(self, name):
        self.name = name
        try:
            self.session_bus = dbus.SessionBus()
            self.player = self.session_bus.get_object('org.mpris.'+name, '/Player')
            self.iface = dbus.Interface(self.player, dbus_interface='org.freedesktop.MediaPlayer')
#            self.iface.connect_to_signal('TrackChange', self.track_change)
        except dbus.exceptions.DBusException as e:
            print(e)
            self.init = False
        else:
            self.init = True
    def track_change(self, sender=None):
        print('track changed, sender =', sender)
    def send(self, cmd, *args):
        if not self.init:
            self.__init__(self.name)
        if not self.init:
            return

        if cmd.lower() == 'playpause':
            cmd = 'Play' if self.iface.GetStatus()[0] else 'Pause'
        elif cmd.lower() == 'repeat':
            args = (self.iface.GetStatus()[2] == 0,)
        print(args, cmd)
        self.iface.__getattr__(cmd)(*args)


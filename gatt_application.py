from dbus_next.service import ServiceInterface, method

class GattApplication(ServiceInterface):
    def __init__(self, path, managed_objects):
        super().__init__('org.freedesktop.DBus.ObjectManager')
        self.path = path
        self.managed_objects = managed_objects

    @method()
    def GetManagedObjects(self) -> 'a{oa{sa{sv}}}':
        return self.managed_objects

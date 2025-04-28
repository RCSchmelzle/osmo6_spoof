from dbus_next.service import ServiceInterface, method

class GattApplication(ServiceInterface):
    def __init__(self, path, service_paths_and_characteristics):
        super().__init__('org.freedesktop.DBus.ObjectManager')  # Correct now
        self.path = path
        self.services_and_chars = service_paths_and_characteristics

    @method()
    def GetManagedObjects(self) -> 'a{oa{sa{sv}}}':
        return self.services_and_chars

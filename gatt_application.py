from dbus_next.service import ServiceInterface, dbus_property

class GattApplication(ServiceInterface):
    def __init__(self, path, service_paths):
        super().__init__('org.bluez.GattApplication1')
        self.path = path
        self.service_paths = service_paths

    @dbus_property()
    def Includes(self) -> 'ao':
        return []  # No included applications

    @Includes.setter
    def Includes(self, value: 'ao'):
        pass  # Setter required, even if unused

    @dbus_property()
    def Services(self) -> 'ao':
        return self.service_paths

    @Services.setter
    def Services(self, value: 'ao'):
        self.service_paths = value

from dbus_next.service import ServiceInterface, dbus_property

class EmptyFF60Service(ServiceInterface):
    def __init__(self, path):
        super().__init__('org.bluez.GattService1')
        self.path = path
        self.uuid = '0000ff60-0000-1000-8000-00805f9b34fb'
        self.primary = True
        self.characteristics = []  # No characteristics!

    @dbus_property()
    def UUID(self) -> 's':
        return self.uuid

    @UUID.setter
    def UUID(self, value: 's'):
        self.uuid = value

    @dbus_property()
    def Primary(self) -> 'b':
        return self.primary

    @Primary.setter
    def Primary(self, value: 'b'):
        self.primary = value

    @dbus_property()
    def Characteristics(self) -> 'ao':
        return []  # No characteristics to return

    @Characteristics.setter
    def Characteristics(self, value: 'ao'):
        pass

    def setup(self, bus):
        bus.export(self.path, self)

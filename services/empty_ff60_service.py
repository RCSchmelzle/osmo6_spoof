from dbus_next.service import ServiceInterface, dbus_property
from characteristics.base_characteristics import SimpleReadCharacteristic

class EmptyFF60Service(ServiceInterface):
    def __init__(self, path):
        super().__init__('org.bluez.GattService1')
        self.path = path
        self.uuid = '0000ff60-0000-1000-8000-00805f9b34fb'
        self.primary = True
        self.characteristics = []

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
        return self.characteristics

    @Characteristics.setter
    def Characteristics(self, value: 'ao'):
        self.characteristics = value

    def setup(self, bus):
        bus.export(self.path, self)

        # Add a DUMMY characteristic
        dummy_char = SimpleReadCharacteristic(
            self.path + '/dummy',
            self.path,
            '0000ff61-0000-1000-8000-00805f9b34fb',
            b'\x00'  # dummy value
        )
        bus.export(dummy_char.path, dummy_char)
        self.characteristics.append(dummy_char.path)

from dbus_next.service import ServiceInterface, method, dbus_property

from characteristics.base_characteristics import SimpleReadCharacteristic

class GenericAccessService(ServiceInterface):
    def __init__(self, path):
        super().__init__('org.bluez.GattService1')
        self.path = path
        self.uuid = '00001800-0000-1000-8000-00805f9b34fb'
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

        # Device Name (0x2A00)
        device_name = SimpleReadCharacteristic(
            self.path + '/device_name',
            self.path,
            '00002a00-0000-1000-8000-00805f9b34fb',
            b'OM6-E05LR2-FAKE'
        )
        bus.export(device_name.path, device_name)
        self.characteristics.append(device_name.path)

        # Appearance (0x2A01)
        appearance = SimpleReadCharacteristic(
            self.path + '/appearance',
            self.path,
            '00002a01-0000-1000-8000-00805f9b34fb',
            (0x03c0).to_bytes(2, byteorder='little')  # 0x03C0 = Generic Gimbal, Example value
        )
        bus.export(appearance.path, appearance)
        self.characteristics.append(appearance.path)

        # Central Address Resolution (0x2AA6)
        central_address_resolution = SimpleReadCharacteristic(
            self.path + '/central_address_resolution',
            self.path,
            '00002aa6-0000-1000-8000-00805f9b34fb',
            (0x01).to_bytes(1, byteorder='little')  # 0x01 = Address resolution supported
        )
        bus.export(central_address_resolution.path, central_address_resolution)
        self.characteristics.append(central_address_resolution.path)

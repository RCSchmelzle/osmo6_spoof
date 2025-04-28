from dbus_next.service import ServiceInterface, dbus_property
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
    def UUID(self, value: 'a'):
        pass  # BlueZ might try to set this, ignore safely
    @dbus_property()
    def Primary(self) -> 'b':
        return self.primary
    @Primary.setter
    def Primary(self, value: 'b'):
        pass  # BlueZ might try to set this, ignore safely

    @dbus_property()
    def Characteristics(self) -> 'ao':
        return [path for path, _ in self.characteristics]

    @Characteristics.setter
    def Characteristics(self, value: 'ao'):
        pass  # BlueZ might try to set this, ignore safely

    def setup(self, bus):
        bus.export(self.path, self)

        device_name = SimpleReadCharacteristic(
            self.path + '/device_name',
            self.path,
            '00002a00-0000-1000-8000-00805f9b34fb',
            b'OM6-E05LR2-FAKE'
        )
        bus.export(device_name.path, device_name)
        self.characteristics.append((device_name.path, device_name))

        appearance = SimpleReadCharacteristic(
            self.path + '/appearance',
            self.path,
            '00002a01-0000-1000-8000-00805f9b34fb',
            (0x03C0).to_bytes(2, byteorder='little')
        )
        bus.export(appearance.path, appearance)
        self.characteristics.append((appearance.path, appearance))

        central_address_resolution = SimpleReadCharacteristic(
            self.path + '/central_address_resolution',
            self.path,
            '00002aa6-0000-1000-8000-00805f9b34fb',
            (0x01).to_bytes(1, byteorder='little')
        )
        bus.export(central_address_resolution.path, central_address_resolution)
        self.characteristics.append((central_address_resolution.path, central_address_resolution))

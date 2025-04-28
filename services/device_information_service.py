from dbus_next.service import ServiceInterface, dbus_property
from characteristics.base_characteristics import SimpleReadCharacteristic

class DeviceInformationService(ServiceInterface):
    def __init__(self, path):
        super().__init__('org.bluez.GattService1')
        self.path = path
        self.uuid = '0000180a-0000-1000-8000-00805f9b34fb'
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
        # Manufacturer Name
        manufacturer = SimpleReadCharacteristic(
            self.path + '/manufacturer',
            self.path,
            '00002a29-0000-1000-8000-00805f9b34fb',
            b'DJI'
        )
        bus.export(manufacturer.path, manufacturer)
        self.characteristics.append(manufacturer.path)

        # Serial Number
        serial = SimpleReadCharacteristic(
            self.path + '/serial',
            self.path,
            '00002a25-0000-1000-8000-00805f9b34fb',
            b'FAKE1234567'
        )
        bus.export(serial.path, serial)
        self.characteristics.append(serial.path)

        # Hardware Revision
        hardware = SimpleReadCharacteristic(
            self.path + '/hardware',
            self.path,
            '00002a27-0000-1000-8000-00805f9b34fb',
            b'OM6'
        )
        bus.export(hardware.path, hardware)
        self.characteristics.append(hardware.path)


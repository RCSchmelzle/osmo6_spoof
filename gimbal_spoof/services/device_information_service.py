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
        return [path for path, _ in self.characteristics]

    @Characteristics.setter
    def Characteristics(self, value: 'ao'):
        pass

    def setup(self, bus):
        bus.export(self.path, self)

        # Only Manufacturer Name
        manufacturer = SimpleReadCharacteristic(
            self.path + '/manufacturer',
            self.path,
            '00002a29-0000-1000-8000-00805f9b34fb',
            b'DJI'
        )
        bus.export(manufacturer.path, manufacturer)
        self.characteristics.append((manufacturer.path, manufacturer))

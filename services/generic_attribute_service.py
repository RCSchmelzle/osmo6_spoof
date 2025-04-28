from dbus_next.service import ServiceInterface, dbus_property
from characteristics.service_changed_characteristic import ServiceChangedCharacteristic

class GenericAttributeService(ServiceInterface):
    def __init__(self, path):
        super().__init__('org.bluez.GattService1')
        self.path = path
        self.uuid = '00001801-0000-1000-8000-00805f9b34fb'
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
        service_changed = ServiceChangedCharacteristic(
            self.path + '/service_changed',
            self.path,
            '00002a05-0000-1000-8000-00805f9b34fb'  # ← UUID for Service Changed characteristic
        )
        bus.export(service_changed.path, service_changed)
        self.characteristics.append(service_changed.path)

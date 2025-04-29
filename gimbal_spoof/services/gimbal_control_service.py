from dbus_next.service import ServiceInterface, dbus_property, method
from characteristics.base_characteristics import SimpleReadCharacteristic, SimpleWriteCharacteristic, SimpleNotifyCharacteristic

class GimbalControlService(ServiceInterface):
    def __init__(self, path):
        super().__init__('org.bluez.GattService1')
        self.path = path
        self.uuid = '0000fff0-0000-1000-8000-00805f9b34fb'
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

        # FFF4: Status Notify
        fff4 = SimpleNotifyCharacteristic(
            self.path + '/fff4',
            self.path,
            '0000fff4-0000-1000-8000-00805f9b34fb'
        )
        bus.export(fff4.path, fff4)
        self.characteristics.append((fff4.path, fff4))

        # FFF5: Command Write (Write Without Response)
        fff5 = SimpleWriteCharacteristic(
            self.path + '/fff5',
            self.path,
            '0000fff5-0000-1000-8000-00805f9b34fb',
            write_props=['write', 'write-without-response']
        )
        bus.export(fff5.path, fff5)
        self.characteristics.append((fff5.path, fff5))

        # FFF3: Control Write/Notify
        fff3 = SimpleWriteCharacteristic(
            self.path + '/fff3',
            self.path,
            '0000fff3-0000-1000-8000-00805f9b34fb',
            write_props=['write', 'notify']
        )
        bus.export(fff3.path, fff3)
        self.characteristics.append((fff3.path, fff3))


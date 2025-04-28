from dbus_next.service import ServiceInterface, dbus_property
from characteristics.base_characteristics import SimpleNotifyCharacteristic, SimpleWriteCharacteristic

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
        return self.characteristics

    @Characteristics.setter
    def Characteristics(self, value: 'ao'):
        self.characteristics = value

    def setup(self, bus):

        bus.export(self.path, self)

        # Notify
        notify = SimpleNotifyCharacteristic(
            self.path + '/fff4',
            self.path,
            '0000fff4-0000-1000-8000-00805f9b34fb'
        )
        bus.export(notify.path, notify)
        notify.setup(bus)  # <<< ADD THIS LINE
        self.characteristics.append(notify.path)

        # Write
        write = SimpleWriteCharacteristic(
            self.path + '/fff5',
            self.path,
            '0000fff5-0000-1000-8000-00805f9b34fb'
        )
        bus.export(write.path, write)
        self.characteristics.append(write.path)

        # Write + Notify
        write_notify = SimpleNotifyCharacteristic(
            self.path + '/fff3',
            self.path,
            '0000fff3-0000-1000-8000-00805f9b34fb'
        )
        bus.export(write_notify.path, write_notify)
        write_notify.setup(bus)
        self.characteristics.append(write_notify.path)

from dbus_next.service import ServiceInterface, dbus_property
from logger import log_event  # LOGGING INSERT
from dbus_next.service import method

class CCCDDescriptor(ServiceInterface):
    def __init__(self, path, characteristic_path):
        super().__init__('org.bluez.GattDescriptor1')
        self.path = path
        self.characteristic_path = characteristic_path
        self.uuid = '00002902-0000-1000-8000-00805f9b34fb'  # Standard CCCD UUID
        self.flags = ['read', 'write']
        self.value = b'\x00\x00'  # Notifications/indications initially disabled

    @dbus_property()
    def UUID(self) -> 's':
        return self.uuid

    @UUID.setter
    def UUID(self, value: 's'):
        self.uuid = value

    @dbus_property()
    def Characteristic(self) -> 'o':
        return self.characteristic_path

    @Characteristic.setter
    def Characteristic(self, value: 'o'):
        self.characteristic_path = value

    @dbus_property()
    def Flags(self) -> 'as':
        return self.flags

    @Flags.setter
    def Flags(self, value: 'as'):
        self.flags = value

    @dbus_property()
    def Value(self) -> 'ay':
        return self.value

    @Value.setter
    def Value(self, value: 'ay'):
        self.value = value

    @method() # added extra
    def WriteValue(self, value: 'ay', options: 'a{sv}'):
        self.value = bytes(value)
        log_event("CCCD_WRITE", self.uuid, self.path, self.value)

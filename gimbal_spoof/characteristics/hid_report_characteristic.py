from dbus_next.service import ServiceInterface, dbus_property, method
from characteristics.cccd_descriptor import CCCDDescriptor  # Reuse the CCCD!

class HIDReportCharacteristic(ServiceInterface):
    def __init__(self, path, service_path, uuid):
        super().__init__('org.bluez.GattCharacteristic1')
        self.path = path
        self.service_path = service_path
        self.uuid = uuid
        self.flags = ['read', 'write', 'notify']
        self.value = b'\x00'  # Initial dummy value
        self.notifying = False
        self.cccd = None  # Client Characteristic Configuration Descriptor

    @dbus_property()
    def UUID(self) -> 's':
        return self.uuid

    @UUID.setter
    def UUID(self, value: 's'):
        self.uuid = value

    @dbus_property()
    def Service(self) -> 'o':
        return self.service_path

    @Service.setter
    def Service(self, value: 'o'):
        self.service_path = value

    @dbus_property()
    def Flags(self) -> 'as':
        return self.flags

    @Flags.setter
    def Flags(self, value: 'as'):
        self.flags = value

    @dbus_property()
    def Notifying(self) -> 'b':
        return self.notifying

    @Notifying.setter
    def Notifying(self, value: 'b'):
        self.notifying = value

    @method()
    def ReadValue(self, options: 'a{sv}') -> 'ay':
        print(f"📖 HID Report Read from {self.uuid}")
        return self.value

    @method()
    def WriteValue(self, value: 'ay', options: 'a{sv}'):
        self.value = bytes(value)
        print(f"✍️ HID Report Write to {self.uuid}: {self.value.hex()}")

    @method()
    def StartNotify(self):
        print(f"🔔 HID Report Start Notify {self.uuid}")
        self.notifying = True

    @method()
    def StopNotify(self):
        print(f"🔕 HID Report Stop Notify {self.uuid}")
        self.notifying = False

    def setup(self, bus):
        self.cccd = CCCDDescriptor(self.path + '/cccd', self.path)
        bus.export(self.cccd.path, self.cccd)

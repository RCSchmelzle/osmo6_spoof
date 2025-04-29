from dbus_next.service import ServiceInterface, dbus_property, method
from characteristics.cccd_descriptor import CCCDDescriptor  # Reuse the CCCD!
from logger import log_event  # LOGGING INSERT

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
        log_event("READ", self.uuid, self.path, self.value)
        return self.value

    @method()
    def WriteValue(self, value: 'ay', options: 'a{sv}'):
        self.value = bytes(value)
        log_event("WRITE", self.uuid, self.path, self.value)

    @method()
    def StartNotify(self):
        log_event("START_NOTIFY", self.uuid, self.path)
        self.notifying = True

    @method()
    def StopNotify(self):
        log_event("STOP_NOTIFY", self.uuid, self.path)
        self.notifying = False


    def setup(self, bus):
        self.cccd = CCCDDescriptor(self.path + '/cccd', self.path)
        bus.export(self.cccd.path, self.cccd)

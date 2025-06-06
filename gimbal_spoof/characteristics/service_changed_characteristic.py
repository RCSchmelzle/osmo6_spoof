from dbus_next.service import ServiceInterface, dbus_property, method
from characteristics.cccd_descriptor import CCCDDescriptor
from logger import log_event  # LOGGING INSERT

class ServiceChangedCharacteristic(ServiceInterface):
    def __init__(self, path, service_path, uuid):
        super().__init__('org.bluez.GattCharacteristic1')
        self.path = path
        self.service_path = service_path
        self.uuid = uuid
        self.flags = ['indicate']
        self.value = b'\x00\x00\x00\x00'
        self.notifying = False
        self.cccd = None

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
    def StartNotify(self):
        log_event("START_INDICATE", self.uuid, self.path)
        self.notifying = True

    @method()
    def StopNotify(self):
        log_event("STOP_INDICATE", self.uuid, self.path)
        self.notifying = False


    def setup(self, bus):
        bus.export(self.path, self)
        self.cccd = CCCDDescriptor(self.path + '/cccd', self.path)
        bus.export(self.cccd.path, self.cccd)

from dbus_next.service import ServiceInterface, method, dbus_property
from logger import log_event  # LOGGING INSERT

class SimpleReadCharacteristic(ServiceInterface):
    def __init__(self, path, service_path, uuid, value):
        super().__init__('org.bluez.GattCharacteristic1')
        self.path = path
        self.service_path = service_path
        self.uuid = uuid
        self.flags = ['read']
        self.value = value

    @dbus_property()
    def UUID(self) -> 's':
        return self.uuid

    @UUID.setter
    def UUID(self, value: 's'):
        pass

    @dbus_property()
    def Service(self) -> 'o':
        return self.service_path

    @Service.setter
    def Service(self, value: 'o'):
        pass

    @dbus_property()
    def Flags(self) -> 'as':
        return self.flags

    @Flags.setter
    def Flags(self, value: 'as'):
        pass

    @method()
    def ReadValue(self, options: 'a{sv}') -> 'ay':
        log_event("READ", self.uuid, self.path, self.value)  # LOGGING INSERT
        return self.value



class SimpleWriteCharacteristic(ServiceInterface):
    def __init__(self, path, service_path, uuid, write_props=['write']):
        super().__init__('org.bluez.GattCharacteristic1')
        self.path = path
        self.service_path = service_path
        self.uuid = uuid
        self.flags = write_props
        self.value = b''

    @dbus_property()
    def UUID(self) -> 's':
        return self.uuid

    @UUID.setter
    def UUID(self, value: 's'):
        pass

    @dbus_property()
    def Service(self) -> 'o':
        return self.service_path

    @Service.setter
    def Service(self, value: 'o'):
        pass

    @dbus_property()
    def Flags(self) -> 'as':
        return self.flags

    @Flags.setter
    def Flags(self, value: 'as'):
        pass

    @method()
    def WriteValue(self, value: 'ay', options: 'a{sv}'):
        self.value = bytes(value)
        log_event("WRITE", self.uuid, self.path, self.value)  # LOGGING INSERT



class SimpleNotifyCharacteristic(ServiceInterface):
    def __init__(self, path, service_path, uuid):
        super().__init__('org.bluez.GattCharacteristic1')
        self.path = path
        self.service_path = service_path
        self.uuid = uuid
        self.flags = ['notify']
        self.notifying = False

    @dbus_property()
    def UUID(self) -> 's':
        return self.uuid

    @UUID.setter
    def UUID(self, value: 's'):
        pass

    @dbus_property()
    def Service(self) -> 'o':
        return self.service_path

    @Service.setter
    def Service(self, value: 'o'):
        pass

    @dbus_property()
    def Flags(self) -> 'as':
        return self.flags

    @Flags.setter
    def Flags(self, value: 'as'):
        pass

    @method()
    def StartNotify(self):
        log_event("START_NOTIFY", self.uuid, self.path)  # LOGGING INSERT
        self.notifying = True

    @method()
    def StopNotify(self):
        log_event("STOP_NOTIFY", self.uuid, self.path)  # LOGGING INSERT
        self.notifying = False



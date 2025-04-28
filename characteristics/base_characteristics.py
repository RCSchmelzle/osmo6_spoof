from dbus_next.service import ServiceInterface, dbus_property, method

class SimpleReadCharacteristic(ServiceInterface):
    def __init__(self, path, service_path, uuid, value_bytes):
        super().__init__('org.bluez.GattCharacteristic1')
        self.path = path
        self.service_path = service_path
        self.uuid = uuid
        self.flags = ['read']
        self.value = value_bytes

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

    @method()
    def ReadValue(self, options: 'a{sv}') -> 'ay':
        print(f"📖 Read from {self.uuid}")
        return self.value

class SimpleWriteCharacteristic(ServiceInterface):
    def __init__(self, path, service_path, uuid):
        super().__init__('org.bluez.GattCharacteristic1')
        self.path = path
        self.service_path = service_path
        self.uuid = uuid
        self.flags = ['write', 'write-without-response']
        self.value = b''

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

    @method()
    def WriteValue(self, value: 'ay', options: 'a{sv}'):
        self.value = bytes(value)
        print(f"✍️ Write to {self.uuid}: {self.value.hex()}")

from dbus_next.service import ServiceInterface, dbus_property, method
from characteristics.cccd_descriptor import CCCDDescriptor  # <- NEW

class SimpleNotifyCharacteristic(ServiceInterface):
    def __init__(self, path, service_path, uuid):
        super().__init__('org.bluez.GattCharacteristic1')
        self.path = path
        self.service_path = service_path
        self.uuid = uuid
        self.flags = ['read', 'notify']
        self.value = b'\x00'
        self.notifying = False
        self.cccd = None  # Placeholder for CCCD

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
        print(f"📖 Read from {self.uuid} (notify-capable)")
        return self.value

    @method()
    def StartNotify(self):
        print(f"🔔 Start Notify on {self.uuid}")
        self.notifying = True

    @method()
    def StopNotify(self):
        print(f"🔕 Stop Notify on {self.uuid}")
        self.notifying = False

    def setup(self, bus):
        # ✨ Attach a CCCD Descriptor when setting up
        self.cccd = CCCDDescriptor(self.path + '/cccd', self.path)
        bus.export(self.cccd.path, self.cccd)

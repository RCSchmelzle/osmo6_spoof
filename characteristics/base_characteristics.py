from dbus_next.service import ServiceInterface, method, dbus_property

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
        print(f"✍️ Write received on {self.uuid}: {self.value.hex()}")

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
        self.notifying = True
        print(f"📢 Notifications started on {self.uuid}")

    @method()
    def StopNotify(self):
        self.notifying = False
        print(f"🛑 Notifications stopped on {self.uuid}")

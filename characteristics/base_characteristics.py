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
    def UUID(self, value: 'a'):
        pass  # BlueZ might try to set this, ignore safely

    @dbus_property()
    def Service(self) -> 'o':
        return self.service_path
    @Service.setter
    def Service(self, value: 'o'):
        pass  # BlueZ might try to set this, ignore safely
    @dbus_property()
    def Flags(self) -> 'as':
        return self.flags
    @Flags.setter
    def Flags(self, value: 'as'):
        pass  # BlueZ might try to set this, ignore safely


    @method()
    def ReadValue(self, options: 'a{sv}') -> 'ay':
        return self.value

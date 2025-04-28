from dbus_next.service import ServiceInterface, dbus_property, method
from characteristics.base_characteristics import SimpleReadCharacteristic, SimpleWriteCharacteristic, SimpleNotifyCharacteristic

class HumanInterfaceDeviceService(ServiceInterface):
    def __init__(self, path):
        super().__init__('org.bluez.GattService1')
        self.path = path
        self.uuid = '00001812-0000-1000-8000-00805f9b34fb'
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

        # HID Information (0x2A4A) - Read only
        hid_info = SimpleReadCharacteristic(
            self.path + '/hid_information',
            self.path,
            '00002a4a-0000-1000-8000-00805f9b34fb',
            b'\x11\x01\x00\x02'  # Example: Version 1.11, Country Code 0x00, Flags 0x02
        )
        bus.export(hid_info.path, hid_info)
        self.characteristics.append((hid_info.path, hid_info))

        # Protocol Mode (0x2A4B) - Read + Write
        protocol_mode = SimpleWriteCharacteristic(
            self.path + '/protocol_mode',
            self.path,
            '00002a4b-0000-1000-8000-00805f9b34fb',
            write_props=['read', 'write']
        )
        bus.export(protocol_mode.path, protocol_mode)
        self.characteristics.append((protocol_mode.path, protocol_mode))

        # HID Control Point (0x2A4C) - Write Without Response
        control_point = SimpleWriteCharacteristic(
            self.path + '/control_point',
            self.path,
            '00002a4c-0000-1000-8000-00805f9b34fb',
            write_props=['write-without-response']
        )
        bus.export(control_point.path, control_point)
        self.characteristics.append((control_point.path, control_point))

        # Report 1 (0x2A4D) - Read, Write, Notify
        report1 = SimpleWriteCharacteristic(
            self.path + '/report1',
            self.path,
            '00002a4d-0000-1000-8000-00805f9b34fb',
            write_props=['read', 'write', 'notify']
        )
        bus.export(report1.path, report1)
        self.characteristics.append((report1.path, report1))

        # Report 2 (0x2A4D) - another Report characteristic
        report2 = SimpleWriteCharacteristic(
            self.path + '/report2',
            self.path,
            '00002a4d-0000-1000-8000-00805f9b34fb',
            write_props=['read', 'write', 'notify']
        )
        bus.export(report2.path, report2)
        self.characteristics.append((report2.path, report2))

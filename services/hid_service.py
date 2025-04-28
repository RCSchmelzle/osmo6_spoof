from dbus_next.service import ServiceInterface, dbus_property
from characteristics.base_characteristics import SimpleReadCharacteristic, SimpleWriteCharacteristic, SimpleNotifyCharacteristic
from characteristics.hid_report_characteristic import HIDReportCharacteristic

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
        return self.characteristics

    @Characteristics.setter
    def Characteristics(self, value: 'ao'):
        self.characteristics = value

    def setup(self, bus):
        bus.export(self.path, self)

        # HID Information (0x2A4A) - Read
        hid_info = SimpleReadCharacteristic(
            self.path + '/hid_info',
            self.path,
            '00002a4a-0000-1000-8000-00805f9b34fb',
            b'\x11\x01\x00\x02'  # HID version 1.11, country code 0, flags 2
        )
        bus.export(hid_info.path, hid_info)
        self.characteristics.append(hid_info.path)

        # Report Map (0x2A4B) - Read
        report_map = SimpleReadCharacteristic(
            self.path + '/report_map',
            self.path,
            '00002a4b-0000-1000-8000-00805f9b34fb',
            b'\x05\x01'  # Placeholder HID Report Descriptor (you can customize later)
        )
        bus.export(report_map.path, report_map)
        self.characteristics.append(report_map.path)

        # HID Control Point (0x2A4C) - Write Without Response
        control_point = SimpleWriteCharacteristic(
            self.path + '/control_point',
            self.path,
            '00002a4c-0000-1000-8000-00805f9b34fb'
        )
        bus.export(control_point.path, control_point)
        self.characteristics.append(control_point.path)

        # HID Report 1 (0x2A4D) - Read, Write, Notify
        report1 = HIDReportCharacteristic(
            self.path + '/report1',
            self.path,
            '00002a4d-0000-1000-8000-00805f9b34fb'
        )
        report1.setup(bus)
        self.characteristics.append(report1.path)

        # HID Report 2 (0x2A4D again) - Read, Write, Notify
        report2 = HIDReportCharacteristic(
            self.path + '/report2',
            self.path,
            '00002a4d-0000-1000-8000-00805f9b34fb'
        )
        report2.setup(bus)
        self.characteristics.append(report2.path)

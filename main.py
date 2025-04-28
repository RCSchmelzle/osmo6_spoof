#!/usr/bin/env python3

import asyncio
from dbus_next.aio import MessageBus
from dbus_next.constants import BusType
import dbus_next
from gatt_application import GattApplication

from services.device_information_service import DeviceInformationService
from services.hid_service import HumanInterfaceDeviceService
from services.gimbal_control_service import GimbalControlService
from services.empty_ff60_service import EmptyFF60Service
from services.generic_access_service import GenericAccessService
from services.generic_attribute_service import GenericAttributeService

from characteristics.base_characteristics import SimpleReadCharacteristic
from characteristics.base_characteristics import SimpleNotifyCharacteristic
from characteristics.base_characteristics import SimpleWriteCharacteristic

class TestAdvertisement:
    def __init__(self, path, service_uuids, local_name):
        self.path = path
        self.service_uuids = service_uuids
        self.local_name = local_name

    def export(self, bus):
        from dbus_next.service import ServiceInterface, dbus_property, method

        class Advertisement(ServiceInterface):
            def __init__(self, outer):
                super().__init__('org.bluez.LEAdvertisement1')
                self.outer = outer

            @dbus_property()
            def Type(self) -> 's':
                return 'peripheral'

            @Type.setter
            def Type(self, value: 's'):
                pass

            @dbus_property()
            def ServiceUUIDs(self) -> 'as':
                return self.outer.service_uuids

            @ServiceUUIDs.setter
            def ServiceUUIDs(self, value: 'as'):
                pass

            @dbus_property()
            def LocalName(self) -> 's':
                return self.outer.local_name

            @LocalName.setter
            def LocalName(self, value: 's'):
                pass

            @dbus_property()
            def Discoverable(self) -> 'b':
                return True

            @Discoverable.setter
            def Discoverable(self, value: 'b'):
                pass

            @method()
            def Release(self):
                print("🔻 Advertisement released.")

        ad = Advertisement(self)
        bus.export(self.path, ad)

# --- Main Program ---
async def main():
    print('📢 If it fails to advertise, toggle Bluetooth off and on and retry.')

    bus = await MessageBus(bus_type=BusType.SYSTEM).connect()

    adapter = bus.get_proxy_object('org.bluez', '/org/bluez/hci0', await bus.introspect('org.bluez', '/org/bluez/hci0'))
    adapter_props = adapter.get_interface('org.freedesktop.DBus.Properties')
    
    gatt_manager = adapter.get_interface('org.bluez.GattManager1')
    ad_manager = adapter.get_interface('org.bluez.LEAdvertisingManager1')

    await adapter_props.call_set('org.bluez.Adapter1', 'Powered', dbus_next.Variant('b', True))
    await adapter_props.call_set('org.bluez.Adapter1', 'Discoverable', dbus_next.Variant('b', True))
    await adapter_props.call_set('org.bluez.Adapter1', 'Pairable', dbus_next.Variant('b', True))
    await adapter_props.call_set('org.bluez.Adapter1', 'Alias', dbus_next.Variant('s', 'OM6-E05LR2-FAKE'))

    adapter_props_data = await adapter_props.call_get_all('org.bluez.Adapter1')
    address = adapter_props_data['Address'].value
    print(f"🔎 Look for BLE device with MAC Address: {address}")

    # === Setup ===
    app_path = '/org/bluez/hci0/test_app'

    services = []

    # Device Information Service
    device_info = DeviceInformationService(app_path + '/device_info')
    bus.export(device_info.path, device_info)
    device_info.setup(bus)
    services.append(device_info)

    # HID Service
    hid_service = HumanInterfaceDeviceService(app_path + '/hid')
    bus.export(hid_service.path, hid_service)
    hid_service.setup(bus)
    services.append(hid_service)

    # Gimbal Control Service
    gimbal_service = GimbalControlService(app_path + '/gimbal')
    bus.export(gimbal_service.path, gimbal_service)
    gimbal_service.setup(bus)
    services.append(gimbal_service)

    # Generic Access Service
    generic_access = GenericAccessService(app_path + '/gap')
    bus.export(generic_access.path, generic_access)
    generic_access.setup(bus)
    services.append(generic_access)

    # Generic Attribute Service
    generic_attribute = GenericAttributeService(app_path + '/gatt')
    bus.export(generic_attribute.path, generic_attribute)
    generic_attribute.setup(bus)
    services.append(generic_attribute)

    # Empty FF60 Service
    empty_service = EmptyFF60Service(app_path + '/ff60')
    bus.export(empty_service.path, empty_service)
    # (No setup needed for Empty Service)
    services.append(empty_service)

    


    # Register GATT Application
    gatt_app = GattApplication(app_path, [s.path for s in services])
    bus.export(gatt_app.path, gatt_app)


    print("🛡 Registering GATT application...")
    await gatt_manager.call_register_application(app_path, {})

    print("✅ GATT Server registered!")

    # BLE Advertisement
    ad = TestAdvertisement('/org/bluez/hci0/test_ad', [
    '0000180a-0000-1000-8000-00805f9b34fb',  # Device Info
    '00001812-0000-1000-8000-00805f9b34fb',  # HID
    '0000fff0-0000-1000-8000-00805f9b34fb',  # Gimbal Commands
    '0000ff60-0000-1000-8000-00805f9b34fb',  # Empty Service
    '00001801-0000-1000-8000-00805f9b34fb'   # Generic Attribute Service
    ], 'OM6-E05LR2-FAKE')


    ad.export(bus)

    print("📢 Registering BLE advertisement...")
    await ad_manager.call_register_advertisement(ad.path, {})
    print("✅ BLE Advertisement registered!")

    while True:
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())

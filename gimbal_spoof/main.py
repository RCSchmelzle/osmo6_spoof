#!/usr/bin/env python3

import asyncio
from dbus_next.aio import MessageBus
from dbus_next.constants import BusType
import dbus_next
from gatt_application import GattApplication
from services.generic_access_service import GenericAccessService
from dbus_next.service import ServiceInterface, dbus_property, method
from services.device_information_service import DeviceInformationService
# --- Minimal Advertisement ---
from dbus_next.service import ServiceInterface, dbus_property, method
from services.empty_ff60_service import EmptyFF60Service
from services.gimbal_control_service import GimbalControlService
from services.hid_service import HumanInterfaceDeviceService
from logger import set_device_address

class TestAdvertisement(ServiceInterface):
    def __init__(self, path, service_uuids, local_name):
        super().__init__('org.bluez.LEAdvertisement1')
        self.path = path
        self.service_uuids = service_uuids
        self.local_name = local_name

    @dbus_property()
    def Type(self) -> 's':
        return 'peripheral'

    @Type.setter
    def Type(self, value: 's'):
        pass

    @dbus_property()
    def ServiceUUIDs(self) -> 'as':
        return self.service_uuids

    @ServiceUUIDs.setter
    def ServiceUUIDs(self, value: 'as'):
        pass

    @dbus_property()
    def LocalName(self) -> 's':
        return self.local_name

    @LocalName.setter
    def LocalName(self, value: 's'):
        pass

    @dbus_property()
    def Discoverable(self) -> 'b':
        return True

    @Discoverable.setter
    def Discoverable(self, value: 'b'):
        pass  # <<< THIS was missing

    @method()
    def Release(self):
        print("🔻 Advertisement released.")

# --- Main Program ---
async def main():
    print('📢 Starting BLE GATT Server...')

    bus = await MessageBus(bus_type=BusType.SYSTEM).connect()

    adapter = bus.get_proxy_object('org.bluez', '/org/bluez/hci0', await bus.introspect('org.bluez', '/org/bluez/hci0'))
    adapter_props = adapter.get_interface('org.freedesktop.DBus.Properties')
    gatt_manager = adapter.get_interface('org.bluez.GattManager1')
    ad_manager = adapter.get_interface('org.bluez.LEAdvertisingManager1')

    await adapter_props.call_set('org.bluez.Adapter1', 'Powered', dbus_next.Variant('b', True))
    await adapter_props.call_set('org.bluez.Adapter1', 'Discoverable', dbus_next.Variant('b', True))
    await adapter_props.call_set('org.bluez.Adapter1', 'Pairable', dbus_next.Variant('b', True))
    await adapter_props.call_set('org.bluez.Adapter1', 'Alias', dbus_next.Variant('s', 'OM6-E05LR2-FAKE1908'))

    adapter_props_data = await adapter_props.call_get_all('org.bluez.Adapter1')
    address = adapter_props_data['Address'].value
    set_device_address(address)
    print(f"🔎 Look for BLE device with MAC Address: {address}")

    app_path = '/org/bluez/hci0/test_app'
    services = []



    device_info = DeviceInformationService(app_path + '/device_info')
    device_info.setup(bus)
    services.append(device_info)

    empty_service = EmptyFF60Service(app_path + '/ff60')
    empty_service.setup(bus)
    services.append(empty_service)

    gimbal_service = GimbalControlService(app_path + '/gimbal')
    gimbal_service.setup(bus)
    services.append(gimbal_service)

    hid_service = HumanInterfaceDeviceService(app_path + '/hid')
    hid_service.setup(bus)
    services.append(hid_service)

    # --- Build managed_objects ---
    managed_objects = {}

    for service in services:
        managed_objects[service.path] = {
            'org.bluez.GattService1': {
                'UUID': dbus_next.Variant('s', service.uuid),
                'Primary': dbus_next.Variant('b', service.primary),
                'Characteristics': dbus_next.Variant('ao', [char_path for char_path, _ in service.characteristics]),
            }
        }
        for char_path, char_obj in service.characteristics:
            managed_objects[char_path] = {
                'org.bluez.GattCharacteristic1': {
                    'UUID': dbus_next.Variant('s', char_obj.uuid),
                    'Service': dbus_next.Variant('o', char_obj.service_path),
                    'Flags': dbus_next.Variant('as', char_obj.flags),
                }
            }

    # --- Register GATT Application ---
    gatt_app = GattApplication(app_path, managed_objects)
    bus.export(gatt_app.path, gatt_app)

    print("🛡 Registering GATT application...")
    await gatt_manager.call_register_application(app_path, {})
    print("✅ GATT Server registered!")

    # --- Setup Advertisement ---
    ad = TestAdvertisement(
    '/org/bluez/hci0/test_ad',
    [
        '0000180a-0000-1000-8000-00805f9b34fb',  # Device Info
        '0000ff60-0000-1000-8000-00805f9b34fb',  # Empty service
        '0000fff0-0000-1000-8000-00805f9b34fb',  # Gimbal control
        '00001812-0000-1000-8000-00805f9b34fb',  # HID service
    ],
    'OM6-E05LR2-FAKE'
    )



    bus.export(ad.path, ad)

    print("📢 Registering BLE advertisement...")
    await ad_manager.call_register_advertisement(ad.path, {})
    print("✅ BLE Advertisement registered!")

    while True:
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())

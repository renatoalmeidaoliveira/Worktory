import asyncio
from worktory import InventoryManager

inventory = InventoryManager('inventory.yml')

all_devices = [device.name for device in inventory]
print(f"All devices: {all_devices}\n\n")
all_async = [device.name for device in inventory.filter(mode='async')]
print(f"All async devices: {all_async}\n\n")
all_sync = [device.name for device in inventory.filter(mode='sync')]
print(f"All sync devices: {all_sync}\n\n")
all_group_core = [device.name for device in inventory.filter(group='CORE')]
print(f"All devices in CORE group: {all_group_core}\n\n")
all_sync_in_CORE = [device.name for device in inventory.filter(group='CORE', mode='sync', filter_mode="AND")]
print(f"All sync devices in CORE group: {all_sync_in_CORE}\n\n")
all_async_in_CORE = [device.name for device in inventory.filter(group='CORE', mode='async', filter_mode="AND")]
print(f"All async devices in CORE group: {all_async_in_CORE}\n\n")
concat_filter = [device.name for device in inventory.filter(group='CORE').filter(mode='async')]
print(f"Concat Filters: {concat_filter}\n\n")

devices_version = {}
async def get_version(dev):
    try:
        await dev.connect()
        output = await dev.parse("show version")
        devices_version[dev.name] = output
    except Exception as e:
        print(e)
    finally:
        await dev.disconnect()
        
async def async_main():
    all_async = [device for device in inventory.filter(group='CORE', mode='async', filter_mode="AND")]
    coros = [get_version(dev) for dev in all_async]
    await asyncio.gather(*coros)

loop = asyncio.get_event_loop()
loop.run_until_complete(async_main())

for device in devices_version:
    print(f"{device} : {devices_version[device]} \n\n")

Using worktory
=======================

Sample Inventory
--------------------------

.. code-block:: python 

    devices = [
                {
                'name': 'sandbox-iosxr-1',
                'hostname': 'sandbox-iosxr-1.cisco.com',
                'platform': 'cisco_iosxr',
                'username': 'admin',
                'password': 'C1sco12345',
                'groups': ['CORE'],
                'connection_manager': 'scrapli',
                'select_parsers' : 'genie',
                'mode': 'async',
                'transport': 'asyncssh',
                },
                {
                'name': 'sandbox-nxos-1',
                'hostname': 'sandbox-nxos-1.cisco.com',
                'platform': 'cisco_nxos',
                'username': 'admin',
                'password': 'Admin_1234!',
                'groups': ['CORE'],
                'select_parsers' : 'ntc',
                'connection_manager': 'scrapli',
                'mode': 'async',
                'transport': 'asyncssh'
                },
                {
                'name': 'sandbox-nxos-2',
                'hostname': 'sandbox-nxos-1.cisco.com',
                'platform': 'nxos',
                'username': 'admin',
                'password': 'Admin_1234!',
                'groups': ['EDGE'],
                'connection_manager': 'unicon',
                'mode': 'sync',
                'transport': 'ssh',
                'GRACEFUL_DISCONNECT_WAIT_SEC': 0,
                'POST_DISCONNECT_WAIT_SEC': 0,
                },
                {
                'name': 'sandbox-iosxr-2',
                'hostname': 'sandbox-iosxr-1.cisco.com',
                'platform': 'cisco_iosxr',
                'username': 'admin',
                'password': 'C1sco12345',
                'groups': ['CORE'],
                'connection_manager': 'scrapli',
                'select_parsers' : 'genie',
                'mode': 'sync',
                },
            ]

Collecting Running config from async devices
-------------------------------------------------------

.. code-block:: python 

    from worktory import InventoryManager
    import asyncio
    inventory = InventoryManager(devices)

    device_configs = {}
    async def get_config(device):
        await device.connect()
        config = await device.execute("show running-config")
        device_configs[device.name] = config
        await device.disconnect()

    async def async_main():
        coros = [get_config(device) for device in inventory.filter(mode='async')]
        await asyncio.gather(*coros)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())


Collecting Running config from sync devices
-------------------------------------------------------

.. code-block:: python 

    from worktory import InventoryManager
    from multiprocessing import Pool
    inventory = InventoryManager(devices)

    def get_config(device_name):
        inventory = InventoryManager(devices)
        device = inventory.devices[device_name]
        device.connect()
        config = device.execute("show running-config")
        device.disconnect()
        return ( device.name , config )

    def main():
        devs = [device.name for device in inventory.filter(mode='sync')]
        with Pool(2) as p:
            return p.map(get_config, devs)

    
    output = main()


    

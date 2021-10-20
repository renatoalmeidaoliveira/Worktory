Parsing
=======================

By default worktory tries to parse the device output in all available parsers, ie, `ntc-templates`, `genie parses`, and custom `textFSM`.

To use custom textFSM devices, create the following directive structure in your working directory.

.. code-block :: bash    

    .
    ├── script.py
    ├── inventory.yml
    ├── parsers         
    ├   ├── platform 
    ├   ├   ├── command.textfsm  
    ├   ├── comware
    ├   ├   ├── display_interfaces.textfsm  
    
.. tip::

    Worktory replace "spaces" by "_" when looking for the appropriated parser

Code example
--------------

sample inventory
^^^^^^^^^^^^^^^^^^

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
                'platform': 'cisco_nxos',
                'username': 'admin',
                'password': 'Admin_1234!',
                'groups': ['EDGE'],
                'connection_manager': 'scrapli',
                'mode': 'sync',
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

Parsing show interfaces
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python 

    >>> from worktory import InventoryManager
    >>> inventory = InventoryManager(devices)
    >>> device = inventory.devices['sandbox-nxos-2']
    >>> device.connect()
    >>> output = device.parse("show version")
    >>> device.disconnect()
    >>> print(output)
    { 'fsm': {
         'fail': "[Errno 2] No such file or directory: '/home/renato/Worktory/parsers/cisco_nxos/show_version.textfsm'"},
     'ntc': {
         'result': [{'uptime': '0 day(s), 6 hour(s), 59 minute(s), 22 second(s)', 'last_reboot_reason': 'Unknown', 'os': '9.3(3)', 'boot_image': 'bootflash:///nxos.9.3.3.bin', 'platform': 'C9300v', 'hostname': 'NXOS-Always-On', 'serial': '9N3KD63KWT0'}]},
     'genie': {
         'result': {'platform': {'name': 'Nexus', 'os': 'NX-OS', 'software': {'system_version': '9.3(3)', 'system_image_file': 'bootflash:///nxos.9.3.3.bin', 'system_compile_time': '12/22/2019 2:00:00 [12/22/2019 14:00:37]'}, 'hardware': {'model': 'Nexus9000 C9300v', 'chassis': 'Nexus9000 C9300v', 'slots': 'None', 'rp': 'None', 'cpu': 'Intel(R) Xeon(R) Gold 6148 CPU @ 2.40GHz', 'memory': '16408988 kB', 'processor_board_id': '9N3KD63KWT0', 'device_name': 'NXOS-Always-On', 'bootflash': '4287040 kB'}, 'kernel_uptime': {'days': 0, 'hours': 6, 'minutes': 59, 'seconds': 22}, 'reason': 'Unknown'}}}}



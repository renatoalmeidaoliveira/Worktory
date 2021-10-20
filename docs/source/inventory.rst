Inventory creation
=======================

Currently, worktory accepts two input types for the inventory creation a `List[Dict]` and an `str` for the inventory file path, and for loading the inventory all you need is:

.. code-block:: python

    Inventory = InventoryManager(“path”)   # or
    Inventory = InventoryManager(devices_list)

Device Object
-----------------

The device object must have the following attributes:

* name
* hostname
* platform
* username
* password
* template_dir
.. tip::

    Directory for custom textFSM templates

* select_parsers

.. tip::

    Supports: ‘genie’, ‘ntc’, ‘fsm’, ‘ALL’, defaults to ‘ALL’
* mode  

.. tip::

    Supports: “sync” or “async”, defaults to “sync”
* parser

.. tip::

    Defaults to “Default”
* connection_manager 

.. tip::

    Supports: ‘scrapli’, ‘unicon’, ‘netmiko’; defaults to ‘scrapli’

And custom attributes depending on which connector plugin, and parser you choose to use.

Unicon connector sample
--------------------------------

.. code-block:: python 

    devices = [{
        'name': 'sandbox-nxos',
        'hostname': 'sandbox-nxos-1.cisco.com',
        'platform': 'nxos',
        'username': 'admin',
        'password': 'Admin_1234!',
        'groups': ['CORE'],
        'connection_manager': 'unicon',
        'mode': 'sync',
        'transport': 'ssh',
    }]
    Inventory = InventoryManager(devices)

Optional attributes:

* 'GRACEFUL_DISCONNECT_WAIT_SEC',
  'POST_DISCONNECT_WAIT_SEC',
  'conn_class',
  'port',
  'enable_password',
  

Netmiko connector sample
--------------------------------

.. code-block:: python 

    devices = [{
        'name': 'sandbox-nxos',
        'hostname': 'sandbox-nxos-1.cisco.com',
        'platform': 'cisco_nxos',
        'username': 'admin',
        'password': 'Admin_1234!',
        'groups': ['CORE'],
        'connection_manager': 'netmiko',
        'mode': 'sync',
        'transport': 'ssh',
    }]
    Inventory = InventoryManager(devices)

Optional attributes:

* 'port',
  'verbose',
  'global_delay_factor',
  'global_cmd_verify',
  'use_keys',
  'key_file',
  'pkey',
  'passphrase',
  'allow_agent',
  'ssh_strict',
  'system_host_keys',
  'alt_host_keys',
  'alt_key_file',
  'ssh_config_file',
  'conn_timeout',
  'auth_timeout',
  'banner_timeout',
  'blocking_timeout',
  'timeout',
  'session_timeout',
  'keepalive',
  'default_enter',
  'response_return',
  'serial_settings',
  'fast_cli',
  'session_log',
  'session_log_record_writes',
  'session_log_file_mode',
  'allow_auto_change',
  'encoding', 

Scrapli sync connector sample
--------------------------------

.. code-block:: python 

    devices = [{
        'name': 'sandbox-nxos',
        'hostname': 'sandbox-nxos-1.cisco.com',
        'platform': 'cisco_nxos',
        'username': 'admin',
        'password': 'Admin_1234!',
        'groups': ['CORE'],
        'connection_manager': 'scrapli',
        'mode': 'sync',
    }]
    Inventory = InventoryManager(devices)

Optional attributes

* 'auth_private_key',
  'auth_private_key_passphrase',
  'auth_strict_key',
  'auth_bypass',
  'timeout_socket',
  'transport',
  'timeout_transport',
  'timeout_ops',
  'comms_prompt_pattern',
  'comms_return_char',
  'ssh_config_file',
  'ssh_known_hosts_file',
  'on_init',
  'on_open',
  'on_close',
  'transport_options',
  'channel_lock',
  'channel_log',
  'channel_log_mode',
  'logging_uid',
  'privilege_levels',
  'default_desired_privilege_level',
  'failed_when_contains',


Scrapli async connector sample
--------------------------------

.. code-block:: python 

    devices = [{
        'name': 'sandbox-nxos',
        'hostname': 'sandbox-nxos-1.cisco.com',
        'platform': 'cisco_nxos',
        'username': 'admin',
        'password': 'Admin_1234!',
        'groups': ['CORE'],
        'connection_manager': 'scrapli',
        'mode': 'async',
        'transport': 'asyncssh'
    }]
    Inventory = InventoryManager(devices)

Optional attributes

* 'auth_private_key',
  'auth_private_key_passphrase',
  'auth_strict_key',
  'auth_bypass',
  'timeout_socket',
  'transport',
  'timeout_transport',
  'timeout_ops',
  'comms_prompt_pattern',
  'comms_return_char',
  'ssh_config_file',
  'ssh_known_hosts_file',
  'on_init',
  'on_open',
  'on_close',
  'transport_options',
  'channel_lock',
  'channel_log',
  'channel_log_mode',
  'logging_uid',
  'privilege_levels',
  'default_desired_privilege_level',
  'failed_when_contains',


Using inventory file
------------------------------

The inventory file uses the yaml syntax, as bellow:

.. code-block:: yaml

    devices:
        'sandbox-nxos':
            'hostname': 'sandbox-nxos-1.cisco.com'
            'platform': 'cisco_nxos'
            'username': 'admin'
            'password': 'Admin_1234!'
            'groups': 
            - 'CORE'
            'connection_manager': 'netmiko'
            'mode': 'sync'
            'transport': 'ssh'

        'sandbox-nxos-1':
            'hostname': 'sandbox-nxos-1.cisco.com'
            'platform': 'cisco_nxos'
            'username': 'admin'
            'password': 'Admin_1234!'
            'groups': 
            - 'CORE'
            'connection_manager': 'scrapli'
            'mode': 'sync'

        'sandbox-nxos-2':
            'hostname': 'sandbox-nxos-1.cisco.com'
            'platform': 'nxos'
            'username': 'admin'
            'password': 'Admin_1234!'
            'groups': 
            - 'CORE'
            'connection_manager': 'unicon'
            'mode': 'sync'
            'transport': 'ssh'
            'GRACEFUL_DISCONNECT_WAIT_SEC': 0
            'POST_DISCONNECT_WAIT_SEC': 0

For load the inventory file just:

.. code-block:: python 

    Inventory = InventoryManager('inventory.yaml')

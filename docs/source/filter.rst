Filtering
=======================

The :meth:`InventoryManager <worktory.inventory.inventory.InventoryManager>` class implements a filter method that searches in every device for any attribute value and returns an iterator.

The returned iterator also implements the filter method which returns itself, that way the filter method can be concatenated to perform complex queries.


Sample Inventory
--------------------------

.. code-block:: python 

    devices = [
                {
                'name': 'sandbox-nxos',
                'hostname': 'sandbox-nxos-1.cisco.com',
                'platform': 'cisco_nxos',
                'username': 'admin',
                'password': 'Admin_1234!',
                'groups': ['CORE'],
                'connection_manager': 'netmiko',
                'select_parsers' : 'genie',
                'mode': 'sync',
                'transport': 'ssh',
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
                }
            ]


Filtering by mode
--------------------------

.. code-block:: python

    >>> from worktory import InventoryManager
    >>> inventory = InventoryManager(devices)
    >>> print([device.name for device in inventory.filter(mode='async')])
    ['sandbox-nxos-1']

Filtering by groups
--------------------------

.. code-block:: python

    >>> from worktory import InventoryManager
    >>> inventory = InventoryManager(devices)
    >>> print([device.name for device in inventory.filter(groups='EDGE')])
    ['sandbox-nxos-2']

Filtering by parsers
--------------------------

.. code-block:: python

    >>> from worktory import InventoryManager
    >>> inventory = InventoryManager(devices)
    >>> print([device.name for device in inventory.filter(select_parsers='ntc')])
    ['sandbox-nxos-2', 'sandbox-nxos-1']

.. tip::

    If select_parsers attribute isn't set worktory default behavior is to use all available parsers 


Filtering by parser and group
-----------------------------------

.. code-block:: python

    >>> from worktory import InventoryManager
    >>> inventory = InventoryManager(devices)
    >>> print([device.name for device in inventory.filter(select_parsers='ntc',
    ...                                                   groups='CORE',
    ...                                                   filter_mode="AND")])
    ['sandbox-nxos-1']

Concatenating filters
-----------------------------------

.. code-block:: python

    >>> from worktory import InventoryManager
    >>> inventory = InventoryManager(devices)
    >>> print([device.name for device in inventory.filter(select_parsers='ntc').filter(groups='CORE')])
    ['sandbox-nxos-1']
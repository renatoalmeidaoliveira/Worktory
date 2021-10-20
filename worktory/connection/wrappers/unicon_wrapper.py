from __future__ import annotations
from typing import TYPE_CHECKING, Dict
if TYPE_CHECKING:
    from worktory.device.device import Device

from worktory.connection.base_wrapper import base_wrapper
from worktory.connection.fabric import ConnectionFabric
from genie.conf.base import Device as genie_device

@ConnectionFabric.register()
class scrapli_wrapper(base_wrapper):
    registry_name: str = 'unicon'

    def configure(self, device: Device) -> Dict[str,str]:
        self.device = device
        self.manager = self
        if device.mode == "async":
            raise UnsuportedMode("Async isn't supported for Unicon")          
        
        device_data = {
           "os": device.platform,
           "credentials": {
               'default' : {
                   'username': device.username,
                   'password': device.password
               },
           },
           'connections': {
               'a': {
                   'protocol': device.transport,
                   "ip": device.hostname,   

               },
           },
        }

        if hasattr(device, 'enable_password'):
            if device.enable_password is not None:
                device_data['credentials']['enable'] = device.enable_password

        if hasattr(device, 'port'):
            device_data['connections']['a']['port'] = device.port

        if hasattr(device, 'conn_class'):
            device_data['connections']['a']['class'] = device.conn_class

        setting_config = ['GRACEFUL_DISCONNECT_WAIT_SEC',
                          'POST_DISCONNECT_WAIT_SEC']
        for config in  setting_config:  
            if hasattr(device, config):
                if 'settings' not in device_data['connections']['a']:
                    device_data['connections']['a']['settings'] = {}                    
                device_data['connections']['a']['settings'][config] = \
                    getattr(device, config)


        self.conn = genie_device(device.name, **device_data)

        mappings = {}
        methods = ['connect', 'disconnect', 'execute', 'configure']
        for method in methods:
            mappings[method] = getattr(self, f"{device.mode}_{method}")
        
        return mappings
        
    @property
    def connected(self):
        return self.conn.connected
      
    def sync_connect(self):
        try:
            log_mode = self.device.log_mode
        except AttributeError:
            log_mode = False
        try:
            learn_mode = self.device.learn_hostname
        except AttributeError:
            learn_mode = True

        self.conn.connect(log_stdout=log_mode, learn_hostname=learn_mode)
    
    def sync_disconnect(self):
        if self.connected:
            self.conn.disconnect()    

    def sync_execute(self, cmd):
        out = self.conn.execute(cmd)
        return out
         
    def sync_configure(self, cmd):
        out = self.conn.configure(cmd)
        return out

class UnsuportedMode(Exception):
    '''
        Raises when try to use async with sync module
    '''
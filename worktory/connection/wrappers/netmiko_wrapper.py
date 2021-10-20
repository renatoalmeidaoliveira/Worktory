from __future__ import annotations
from typing import TYPE_CHECKING, Dict
if TYPE_CHECKING:
    from worktory.device.device import Device

from worktory.connection.base_wrapper import base_wrapper
from worktory.connection.fabric import ConnectionFabric
from netmiko import ConnectHandler

@ConnectionFabric.register()
class scrapli_wrapper(base_wrapper):
    registry_name: str = 'netmiko'

    def configure(self, device: Device) -> Dict[str,str]:
        self.device = device
        self.manager = self
        if device.mode == "async":
            raise UnsuportedMode("Async isn't supported for Unicon")     

        device_data = {
           "host": device.hostname,
           "username": device.username,
           "password": device.password,
           "device_type": device.platform,
           "auto_connect": False,
        }
        if hasattr(device, 'enable_password'):
            device_data['secret'] = device.enable_password
        
        scrapli_args = [
            'port',
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
        ]
        for arg in scrapli_args:
            if hasattr(device, arg):
                device_data[arg] = getattr(device, arg)
        
        mode = "sync"
        self.conn = ConnectHandler(**device_data)

        mappings = {}
        methods = ['connect',
                   'disconnect',
                   'execute',
                   'configure',
                   'enable',
                   'config_mode',
                   ]
        for method in methods:
            mappings[method] = getattr(self, f"{mode}_{method}")
        
        return mappings
        
    @property
    def connected(self):
        return self.conn.is_alive()
      
    def sync_connect(self):
        self.conn.establish_connection()
    
    def sync_disconnect(self):
        if self.connected:
            self.conn.disconnect()    

    def sync_enable(self):
        self.conn.enable()

    def sync_config_mode(self):
        self.conn.config_mode()

    def sync_execute(self, cmd):        
        out = self.conn.send_command(cmd)
        return out
         
    def sync_configure(self, cmd):
        out = self.conn.send_config_set(cmd)
        return out



class UnsuportedMode(Exception):
    '''
        Raises when try to use async with sync module
    '''
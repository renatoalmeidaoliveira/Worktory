from __future__ import annotations
from typing import TYPE_CHECKING, Dict
if TYPE_CHECKING:
    from worktory.device.device import Device

from worktory.connection.base_wrapper import base_wrapper
from worktory.connection.fabric import ConnectionFabric
from scrapli import Scrapli, AsyncScrapli

@ConnectionFabric.register()
class scrapli_wrapper(base_wrapper):
    registry_name: str = 'scrapli'

    def configure(self, device: Device) -> Dict[str,str]:
        self.device = device
        self.manager = self

        device_data = {
           "host": device.hostname,
           "auth_username": device.username,
           "auth_password": device.password,
           "auth_strict_key": False,
           "platform": device.platform,
        }
        if hasattr(device, 'enable_password'):
            device_data['auth_secondary'] = device.enable_password
        
        scrapli_args = [
            'auth_private_key',
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
        ]
        for arg in scrapli_args:
            if hasattr(device, arg):
                device_data[arg] = getattr(device, arg)
        
        if device.mode == "async":
            mode = "async"
            self.conn = AsyncScrapli(**device_data)

        else:
            mode = "sync"
            self.conn = Scrapli(**device_data)

        mappings = {}
        methods = ['connect', 'disconnect', 'execute', 'configure']
        for method in methods:
            mappings[method] = getattr(self, f"{mode}_{method}")
        
        return mappings
        
    @property
    def connected(self):
        return self.conn.isalive()
      
    async def async_connect(self):
        return await self.conn.open()

    async def async_disconnect(self):
        if self.connected:
            await self.conn.close()    

    async def async_execute(self, cmd):
        out = await self.conn.send_command(cmd)
        return out.result
         
    async def async_configure(self, cmd):
        out = await self.conn.send_configs(cmd)
        return out.result

    def sync_connect(self):
        self.conn.open()
    
    def sync_disconnect(self):
        if self.connected:
            self.conn.close()    

    def sync_execute(self, cmd):
        out = self.conn.send_command(cmd)
        return out.result
         
    def sync_configure(self, cmd):
        out = self.conn.send_configs(cmd)
        return out.result

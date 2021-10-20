from __future__ import annotations
from typing import Any, Dict, List
from worktory.device.device import Device
import yaml

class InventoryManager():
    def __init__(self, inventory_src: Dict = None) -> None:
        self.devices: Dict[str, Device] = {}
        if isinstance(inventory_src, str):
            stream = open(inventory_src, 'r')
            yml_inv = yaml.load(stream, yaml.Loader)
            stream.close()
            devices = []
            for device in yml_inv['devices']:
                dev_dict = yml_inv['devices'][device]
                dev_dict['name'] = device
                devices.append(dev_dict)
            self.load(devices)
        elif isinstance(inventory_src, list):
            self.load(inventory_src)        

    def load(self, inventory_dict: Dict) -> None :
        for device in inventory_dict:
            dev = Device(**device)
            if dev.name not in self.devices:
                self.devices[dev.name] = dev
            else:
                raise DuplicateError(f"Duplicate device name {dev.name}")

    def filter(self, filter_mode: str = "OR", **kwargs):
        device_names = [dev for dev in self.devices]
        return DeviceIterator(device_names, self).filter(filter_mode, **kwargs)

    def add_device(self, device_data: Any):
        if isinstance(device_data, Device):
            device_name = device_data.name
            device = device_data
        elif isinstance(device_data, Dict):
            device = Device(**device_data)
            device_name = device.name
            
        if device_name in self.devices:
            raise DuplicateError("Device {device_name} already exists")
        else:
            self.devices[device_name] = device

    def del_device(self, device_name):
        device = self.devices[device_name]
        self.devices.pop(device_name, None)
        device.destroy()
        del device
        
    def __iter__(self):
        device_names = [dev for dev in self.devices]
        return DeviceIterator(device_names, self)



class DeviceIterator():
    def __init__(self, device_names: List[str], inventory: InventoryManager) -> None:
        self.devices = inventory.devices
        self.dev_list = device_names

    def filter(self, filter_mode: str = "OR", **kwargs ):
        if filter_mode not in ["AND", "OR"]:
            raise Exception("Invalid filter_mode")
        device_names = self.dev_list
        devices = [self.devices[name] for name in device_names]
        filtred_devices = []
        filtred_devices_names = []
        for arg in kwargs:
            for device in devices:
                try:
                    if arg == 'connection_manager':
                        value = device.connection_manager.registry_name
                    else:
                        value = getattr(device, arg)
                    if isinstance(value, list):
                        if kwargs[arg] in value:
                            if device.name not in filtred_devices_names:
                                filtred_devices_names.append(device.name)
                                filtred_devices.append(device)
                    elif isinstance(value, str):
                        if value == kwargs[arg]:
                            if device.name not in filtred_devices_names:
                                filtred_devices_names.append(device.name)
                                filtred_devices.append(device)
                except Exception as e:
                    pass
        
        temp_filtred_devices = filtred_devices_names.copy()
        if filter_mode == "AND":
            for arg in kwargs:
                for device_name in temp_filtred_devices:
                    device = self.devices[device_name]
                    if arg == 'connection_manager':
                        value = device.connection_manager.registry_name
                    else:
                        value = getattr(device, arg)
                    try:
                        if isinstance(value, list):
                            if kwargs[arg] not in value:
                                filtred_devices_names.remove(device_name)
                        elif isinstance(value, str):
                            if value != kwargs[arg]:
                                filtred_devices_names.remove(device_name)                          
                    except Exception:
                        filtred_devices_names.remove(device_name)
        
        self.dev_list = filtred_devices_names
        return self
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            dev_name = self.dev_list.pop()
            return self.devices[dev_name]
        except IndexError:
            raise StopIteration



class DuplicateError(Exception):
    '''
        Raises when device has duplicated name
    '''

            
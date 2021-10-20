from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Dict, List
if TYPE_CHECKING:
    from worktory.device.device import Device



class base_wrapper():

    required_interfaces: List[str] = ['connect', 'disconnect', 'execute', 'configure']

    def __init__(self, device: Device):
        
        mappings = self.configure(device)

        for method in base_wrapper.required_interfaces:
            if method not in mappings:
                raise MethodNotImplemented(f"Required method: {method} not implemented")
        
        for method in mappings:
            setattr(device, method, mappings[method])
        
    def configure(self, device: Device) -> Dict[str,Callable]:
        raise Exception("Method configure not implemented")


    

class MethodNotImplemented(Exception):
    '''
        Raises when wrapper doesn't implement
    '''
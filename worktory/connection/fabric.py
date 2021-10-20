from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from worktory.device.device import Device


class ConnectionFabric():

    registry = {}

    @classmethod
    def register(cls):

        def inner_wrapper(wrapped_class):
            name = wrapped_class.registry_name
            if name in cls.registry:
                raise AlreadyRegistred(f"{name} already registred")
            else:
                cls.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def get_CM(cls, device: Device):
        connection_manager = device.connection_manager
        if connection_manager not in cls.registry:
            raise Exception(f"{connection_manager} not registred")

        exec_class = cls.registry[connection_manager]
        conn_manager = exec_class(device)
        return conn_manager

class AlreadyRegistred(Exception):
    '''
        Raises when tries to register an already registred connection_manager
    '''


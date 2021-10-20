from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from worktory.device.device import Device


class ParserFabric():
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
    def get_parser(cls, device: Device):
        parser = device.parser
        if parser not in cls.registry:
            raise Exception(f"{parser} not registred")

        exec_class = cls.registry[parser]
        parser_manager = exec_class(device)
        return parser_manager

class AlreadyRegistred(Exception):
    '''
        Raises when tries to register an already registred parser
    '''

        
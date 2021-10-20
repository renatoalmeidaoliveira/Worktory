from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List
import asyncio

from worktory.parsers.fabric import ParserFabric
from worktory.connection.fabric import ConnectionFabric



class Device():
    name: str
    hostname: str
    platform: str
    username: str
    password: str
    select_parsers: Any = "ALL"
    transport: str = None
    groups: List[str] = []
    mode: str = 'async'
    parser: str = 'Default'
    connection_manager: str = 'scrapli'
    port: int = None
    enable_password: str = None
    ntc_platform: str = None
    genie_platform: str = None
    fsm_platform: str = None
    
    def __init__(self, **kwargs) -> None:
        for attr in kwargs:
            setattr(self, attr, kwargs[attr])
        for attr in Device.__annotations__:
            if attr not in kwargs:
                try:
                    getattr(self, attr)
                except AttributeError:
                    raise MissingAttribute(f"Missing required attribute: {attr}")

        if self.select_parsers == "ALL":
            self.select_parsers = ['fsm','ntc','genie']
                    
        self.parser_manager = ParserFabric().get_parser(self).manager
        self.connection_manager = ConnectionFabric().get_CM(self).manager

    def destroy(self):
        if self.mode == 'async':
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.disconnect())
        else:
            self.disconnect()

        del self.parser_manager
        del self.connection_manager
        

class MissingAttribute(Exception):
    ''' 
        Raises when Device __annotations__ attributes are missing when instantiating
        the object( required attributes )
    '''

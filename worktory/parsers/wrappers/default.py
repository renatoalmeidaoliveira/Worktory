from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Dict

from worktory.parsers.base_parser import base_parser
if TYPE_CHECKING:
    from worktory.device.device import Device

from genie.conf.base import Device as genie_device
from ntc_templates.parse import parse_output as ntc_parse
import textfsm

from worktory.parsers.fabric import ParserFabric
import os
import asyncio

@ParserFabric.register()
class default_wrapper(base_parser):
    registry_name: str = 'Default'

    def configure(self, device: Device) -> Dict[str, Callable]:
        self.device = device
        self.manager = self
        platform = device.fsm_platform or device.platform

        if hasattr(device, "template_dir"):
            self.templates_dir = f"{device.template_dir}/{platform}"
        else:
            self.templates_dir = f"{os.getcwd()}/parsers/{platform}"
        if device.mode == "async":
            mode = "async"
        else:
            mode = "sync"
        
        platform_translation = {
            "hp_comware": 'comware',
            'cisco_iosxe': 'iosxe',
            'cisco_iosxr': 'iosxr',
            'cisco_nxos': 'nxos',
            'juniper_junos': 'junos',
        }
        if device.platform in platform_translation:
            platform = platform_translation[device.platform]
            
        
        
        self.genie_device = genie_device(device.name,
                                         custom={"abstraction": {"order": ["os"]}},
                                         os=device.genie_platform or platform)
        mappings = {}

        mappings['parse'] =  getattr(self, f"{mode}_parse")
        return mappings
        
    def sync_parse(self, command: str) -> Dict:
        output = {}
        cmd_output = self.device.execute(command)
        output = self._parser(command=command, cmd_output=cmd_output)
        return output
    
    async def async_parse(self, command: str) -> Dict:
        output = {}
        cmd_output = await self.device.execute(command)
        output = self._parser(command=command, cmd_output=cmd_output)
        return output

    def _parser(self, command:str, cmd_output:str):
        device = self.device
        know_parsers = ['fsm','ntc','genie']
        scheduled_parsers = []
        if isinstance(device.select_parsers, str):
            if device.select_parsers == "ALL":
                scheduled_parsers = know_parsers
            elif device.select_parsers in know_parsers:
                scheduled_parsers = [device.select_parsers]
            else:
                raise UnknownParser(f"Unknown parser {device.select_parsers}")
        elif isinstance(device.select_parsers, list):
            for parser_name in device.select_parsers:
                if parser_name in know_parsers:
                    if(parser_name not in scheduled_parsers):
                        scheduled_parsers.append(parser_name)
                else:
                    raise UnknownParser(f"Unknown parser {parser_name}")
        else:
            raise TypeError("select_parser must be str or list")
        
        result = {}
        for parser_name in scheduled_parsers:
            parser_func = getattr(self, f"_{parser_name}_parser")
            result[parser_name] = parser_func(command=command, cmd_output=cmd_output)
        
        return result

    def _genie_parser(self, command:str, cmd_output:str):
        result = {}
        try:
            parsed = self.genie_device.parse(command, output=cmd_output)
            result['result'] = parsed
        except Exception as e:
             result['fail'] = str(e)
        return result        

    def _fsm_parser(self, command:str, cmd_output:str):
        result = {}
        try:
            filename = command.replace(" ", "_")
            template_file = open(f"{self.templates_dir}/{filename}.textfsm")
            fsm = textfsm.TextFSM(template_file)
            parsed = fsm.ParseText(cmd_output)
            template_file.close()
            result['result'] = parsed
        except Exception as e:
             result['fail'] = str(e)        
        return result

    def _ntc_parser(self, command:str, cmd_output: str):
        result = {}
        try:
            parsed = ntc_parse(platform=self.device.ntc_platform or self.device.platform,
                               command=command, data=cmd_output)
            result['result'] = parsed
        except Exception as e:
             result['fail'] = str(e)   
        return result



    

            

class Unconnected(Exception):
    '''
        Raises when try to execute on unconnected Devices
    '''

class UnknownParser(Exception):
    '''
        Raises when try to load an Unknown Parser
    '''
from common.abstracts import MalParserBase
from structs.njrat_0_11g import Njrat011g
from lib.struct_formatter import dive_struct
from base64 import b64decode


class MalParser(MalParserBase):
    def __init__(self):
        super().__init__()
        self.cfg_structs = Njrat011g
        self.magic = b'CompilationRelaxationsAttribute\x00\x00\x01\x00'
        self.cfg_start_offset = 35
        self.cfg_size = 0x300
        self.json_key = [
            'c2_lists', 'directory', 'exe_name', 'process_protected',
            'registry_startup', 'mutex', 'reg_key', 'b64_victim_name',
            'version'
        ]

    def make_json(self):
        self.pretty_cfg = {}
        # fix optional
        if 'type1' in self.raw_cfg.__dict__:
            value = self.raw_cfg.__dict__['type1']
            self.raw_cfg.__dict__.update(value.__dict__)
            value = self.raw_cfg.__dict__['optional']
            del self.raw_cfg.__dict__['optional']
            self.raw_cfg.__dict__['registry_startup'] = value
        elif 'type2' in self.raw_cfg.__dict__:
            value = self.raw_cfg.__dict__['type2']
            self.raw_cfg.__dict__.update(value.__dict__)
            value = self.raw_cfg.__dict__['optional']
            del self.raw_cfg.__dict__['optional']
            self.raw_cfg.__dict__['reg_key'] = value

        for key in self.raw_cfg.__dict__:
            if key not in self.json_key:
                continue
            value = self.raw_cfg.__dict__[key]
            dict_strcut = dive_struct(key, value)
            if 'b64_victim_name' in key:
                value = b64decode(dict_strcut[key])
                self.pretty_cfg[key] = value
            else:
                self.pretty_cfg.update(dict_strcut)

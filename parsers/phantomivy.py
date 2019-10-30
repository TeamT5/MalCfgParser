from common.abstracts import MalParserBase
from structs.phantomivy import Phantomivy
from lib.validator import is_valid_host


class MalParser(MalParserBase):
    def __init__(self):
        super().__init__()
        self.cfg_structs = Phantomivy
        self.cfg_size = 0x300
        self.cfg_start_offset = -0x12c
        self.magic = b'\x00' * 0x50 + b'\xff' * 0x4 + b'\x00' * 0x50
        self.json_key = ['password', 'cnc', 'mutex']

    def make_json(self):
        self.pretty_cfg = {}
        for key in self.json_key:
            if key == 'mutex':
                self.pretty_cfg[key] = self.raw_cfg.mutex
                continue
            value = self.raw_cfg.__dict__[key]
            if isinstance(value, str):
                value = value.replace('\x00', '')
            if 'list' in str(type(value)):
                if 'Cnc' in str(type(value[0])):
                    for idx, v in enumerate(value):
                        if v.port != 0:
                            self.pretty_cfg['cnc' + str(idx) +
                                            '_type'] = v.type
                            self.pretty_cfg['cnc' + str(idx) +
                                            '_port'] = v.port
                            self.pretty_cfg['cnc' + str(idx) +
                                            '_host'] = v.host.replace(
                                                '\x00', '')
            else:
                self.pretty_cfg[key] = value

    def validate(self, cfg):
        if is_valid_host(cfg.cnc[0].host):
            return True
        return False

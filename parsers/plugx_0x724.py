from common.abstracts import MalParserBase
from structs.plugx_0x724 import Plugx_0x724
from lib.validator import is_valid_host


class MalParser(MalParserBase):
    def __init__(self):
        super().__init__()
        self.cfg_structs = Plugx_0x724
        self.cfg_size = 0x724
        self.cfg_start_offset = 0x25c4
        self.magic = b'O\x00l\x00S\x00t\x00a\x00r\x00t\x00P\x00r\x00o\x00c\x00'
        self.json_key = [
            'flag',
            'installname',
            'cnc'
        ]

    def make_json(self):
        self.pretty_cfg = {}
        for key in self.json_key:
            value = self.raw_cfg.__dict__[key]
            if isinstance(value, str):
                value = value.replace('\x00', '')
            if 'list' in str(type(value)):
                if 'Cnc' in str(type(value[0])):
                    for idx, v in enumerate(value):
                        if v.port != 0:
                            self.pretty_cfg['cnc' + str(idx) +
                                            '_proto'] = v.proto.name.upper()
                            self.pretty_cfg['cnc' + str(idx) +
                                            '_port'] = v.port
                            self.pretty_cfg['cnc' + str(idx) +
                                            '_host'] = v.host.replace(
                                                '\x00', '')
            else:
                self.pretty_cfg[key] = value

    def validate(self, cfg):
        if is_valid_host(cfg.cnc[0].host) or is_valid_host(
                cfg.cnc[1].host) or is_valid_host(
                    cfg.cnc[2].host) or is_valid_host(cfg.cnc[3].host):
            return True
        return False

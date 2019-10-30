from common.abstracts import MalParserBase
from structs.keyboy import Keyboy
from lib.validator import is_valid_host


class MalParser(MalParserBase):
    def __init__(self):
        super().__init__()
        self.cfg_structs = Keyboy
        self.magic = b'MDDEFGEGETGIZ'
        self.cfg_start_offset = 0x0
        self.cfg_size = 0x440
        self.json_key = [
            'reverse_host_1', 'reverse_host_2', 'reverse_host_3',
            'reverse_port_1', 'reverse_port_2', 'reverse_port_3',
            'payload_url_1', 'payload_url_2', 'payload_url_3', 'control_port',
            'login_password', 'campaign_code', 'usb'
        ]

    def make_json(self):
        self.pretty_cfg = {}
        for key in self.raw_cfg.__dict__:
            if key not in self.json_key:
                continue
            value = self.raw_cfg.__dict__[key]
            self.pretty_cfg[key] = value.replace('\x00', '')

    def validate(self, cfg):
        if is_valid_host(cfg.reverse_host_1) or is_valid_host(
                cfg.reverse_host_2) or is_valid_host(cfg.reverse_host_3):
            return True
        return False

import re


class MalParserBase(object):
    def __init__(self):
        self.cfg_structs = None
        self.magic = None
        self.cfg_size = None
        self.cfg_start_offset = None  # offset of cfg start to magic
        self.dynamic_size = None
        self.try_decode = None
        self.raw_cfg = None
        self.pretty_cfg = {}

    def __find_magic(self, memblock):
        return [m.start() for m in re.finditer(self.magic, memblock)]

    def __parse(self, cfg_blob):
        cfg = self.cfg_structs.from_bytes(cfg_blob)
        return cfg

    def __dynamic_cfg_size(self, config_blob):
        i = 0
        while True:
            self.cfg_size, skipped_bytes = self.get_cfg_size(config_blob[i:])
            if self.cfg_size > len(config_blob):
                i = i + 1
                continue
            start_offset = i + skipped_bytes
            trim_config_blob = config_blob[start_offset:start_offset +
                                           self.cfg_size]

            if self.try_decode:
                trim_config_blob = self.cfg_decode(trim_config_blob)

            try:
                cfg = self.__parse(trim_config_blob)
                if cfg and self.validate(cfg):
                    self.raw_cfg = cfg
                    self.make_json()
                    return True
            except UnicodeDecodeError:
                pass
            except EOFError:
                pass
            i = i + 1
        return False

    def __fixed_cfg_size(self, config_blob):
        # auto brute force
        for i in range(len(config_blob) + 1 - self.cfg_size):
            if (self.cfg_size + i) > len(config_blob):
                break

            trim_config_blob = config_blob[i:self.cfg_size + i]

            if self.try_decode:
                trim_config_blob = self.cfg_decode(trim_config_blob)

            try:
                cfg = self.__parse(trim_config_blob)
                if cfg and self.validate(cfg):
                    self.raw_cfg = cfg
                    self.make_json()
                    return True
            except Exception:
                pass

    def cfg_parse(self, config_blob):
        if self.dynamic_size:
            return self.__dynamic_cfg_size(config_blob)
        else:
            return self.__fixed_cfg_size(config_blob)

    def mem_parse(self, memblock):
        index_list = self.__find_magic(memblock)
        # print(index_list)
        for index in index_list:
            cfg_start_try = index + self.cfg_start_offset
            if cfg_start_try < 0:
                cfg_start_try = 0
            if self.cfg_parse(memblock[cfg_start_try:]):
                break

    def make_json(self):
        raise NotImplementedError()

    def validate(self, cfg):
        return True

    def cfg_decode(self, blob):
        if self.try_decode:
            raise NotImplementedError()
        return blob

    def get_cfg_size(self, blob):
        if self.get_cfg_size:
            raise NotImplementedError()
        return 0

# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Plugx_0x724(KaitaiStruct):

    class Protocol(Enum):
        unknown = 0
        tcp = 1
        http = 2
        tcp_http = 3
        udp = 4
        tcp_udp = 5
        http_udp = 6
        tcp_http_udp = 7
        icmp = 8
        dns = 16
        unknown2 = 31
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.flag = self._io.read_u4le()
        self.installname = (self._io.read_bytes(256)).decode(u"ASCII")
        self.cnc = [None] * (4)
        for i in range(4):
            self.cnc[i] = self._root.Cnc(self._io, self, self._root)


    class Cnc(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.proto = self._root.Protocol(self._io.read_u2le())
            self.port = self._io.read_u2le()
            self.host = (self._io.read_bytes(192)).decode(u"ASCII")




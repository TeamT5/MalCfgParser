# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO

if parse_version(ks_version) < parse_version('0.7'):
    raise Exception(
        "Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s"
        % (ks_version))


class Keyboy(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = (self._io.read_bytes(64)).decode(u"ASCII")
        self.reverse_host_1 = (self._io.read_bytes(64)).decode(u"ASCII")
        self.reverse_host_2 = (self._io.read_bytes(64)).decode(u"ASCII")
        self.reverse_host_3 = (self._io.read_bytes(64)).decode(u"ASCII")
        self.reverse_port_1 = (self._io.read_bytes(64)).decode(u"ASCII")
        self.reverse_port_2 = (self._io.read_bytes(64)).decode(u"ASCII")
        self.reverse_port_3 = (self._io.read_bytes(64)).decode(u"ASCII")
        self.payload_url_1 = (self._io.read_bytes(128)).decode(u"ASCII")
        self.payload_url_2 = (self._io.read_bytes(128)).decode(u"ASCII")
        self.payload_url_3 = (self._io.read_bytes(128)).decode(u"ASCII")
        self.control_port = (self._io.read_bytes(64)).decode(u"ASCII")
        self.login_password = (self._io.read_bytes(64)).decode(u"ASCII")
        self.campaign_code = (self._io.read_bytes(64)).decode(u"ASCII")
        self.usb = (self._io.read_bytes(64)).decode(u"ASCII")
# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Phantomivy(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.password = (self._io.read_bytes(16)).decode(u"ASCII")
        self.unused = self._io.read_bytes(55)
        self.cnc_count = self._io.read_u4le()
        self.cnc = [None] * ((self.cnc_count + 1))
        for i in range((self.cnc_count + 1)):
            self.cnc[i] = self._root.Cnc(self._io, self, self._root)


    class Cnc(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len = self._io.read_u1()
            self.host = (self._io.read_bytes(self.len)).decode(u"ASCII")
            self.type = self._io.read_u1()
            self.port = self._io.read_u2le()


    @property
    def mutex(self):
        if hasattr(self, '_m_mutex'):
            return self._m_mutex if hasattr(self, '_m_mutex') else None

        io = self._root._io
        _pos = io.pos()
        io.seek(694)
        self._m_mutex = (io.read_bytes(9)).decode(u"ASCII")
        io.seek(_pos)
        return self._m_mutex if hasattr(self, '_m_mutex') else None



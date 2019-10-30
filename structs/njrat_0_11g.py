# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Njrat011g(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.c2_size = self._io.read_u1()
        self.c2_lists = (self._io.read_bytes(self.c2_size)).decode(u"UTF-8")
        self.directory = self._root.UnicodeString(self._io, self, self._root)
        self.exe_name = self._root.UnicodeString(self._io, self, self._root)
        self.process_protected = self._root.UnicodeString(self._io, self, self._root)
        self.optional = self._root.UnicodeString(self._io, self, self._root)
        if self.optional.len > 11:
            self.type2 = self._root.Type2(self._io, self, self._root)

        if self.optional.len <= 11:
            self.type1 = self._root.Type1(self._io, self, self._root)


    class Type1(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.mutex = self._root.UnicodeString(self._io, self, self._root)
            self.reg_key = self._root.UnicodeString(self._io, self, self._root)
            self.b64_victim_name = self._root.UnicodeString(self._io, self, self._root)
            self.version = self._root.UnicodeString(self._io, self, self._root)


    class Type2(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.reg_key = self._root.UnicodeString(self._io, self, self._root)
            self.b64_victim_name = self._root.UnicodeString(self._io, self, self._root)
            self.version = self._root.UnicodeString(self._io, self, self._root)


    class UnicodeString(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len = self._io.read_u1()
            self.val = (self._io.read_bytes(self.len)).decode(u"UTF-8")




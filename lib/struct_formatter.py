from enum import Enum

def dive_struct(key, obj):
    dict_struct = {}
    if 'AsciiString' in str(type(obj)):
        dict_struct = {key: obj.val.rstrip('\x00')}
    elif 'UnicodeString' in str(type(obj)):
        dict_struct = {key: obj.val.replace('\x00','')}
    elif isinstance(obj,str):
        dict_struct = {key: obj.replace('\x00','')}
    elif isinstance(obj,Enum):
        dict_struct = {key: obj.name.upper()}
    elif hasattr(obj, '__dict__'):
        for key in obj.__dict__:
            if key.startswith('_'):
                continue
            dict_struct[key] = dive_struct(key, obj.__dict__[key])
    else:
        dict_struct = {key: obj}
    return dict_struct
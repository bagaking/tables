# -*- coding: utf-8 -*

def to_int(val):
    if isinstance(val, str):
        val = val.strip().lower().replace(' ', '')
        if val.startswith("0x") or val.startswith("-0x"):
            return int(val,16)
        elif val.startswith("0") or val.startswith("-0"):
            return int(val,8)
        else:
            return int(val)
    else:
        return int(val)

def to_uint(val):
    num = to_int(val)
    if num < 0:
        raise Exception("convertor error: val cannot be negative.", num)
    return num

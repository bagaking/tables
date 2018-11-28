# -*- coding: utf-8 -*

def toint(val):
    if isinstance(val, str):
        if val.startswith("0x") or val.startswith("0X"):
            return int(val,16)
        elif val.startswith("0"):
            return int(val,8)
        else:
            return int(val)
    else:
        return int(val)
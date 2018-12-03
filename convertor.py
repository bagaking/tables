# -*- coding: utf-8 -*
import types

def to_int(val):
    val_type = type(val)
    if val_type is str:
        val = val.strip().lower().replace(' ', '')
        if val.startswith("0x") or val.startswith("-0x"):
            return int(val,16)
        elif val.startswith("0") or val.startswith("-0"):
            return int(val,8)
        else:
            return int(val)
    elif val_type is int:
        return int(val)
    elif val_type is float:
        num = int(val)
        if num != val:
            print("convertor to_int warning: the variable %s type is float." % val)
        return int(val)
    else:
        print("convertor to_int warning: the variable type is not any of int, float, string, please check.")
        return int(val)

def to_uint(val):
    num = to_int(val)
    if num < 0:
        raise Exception("convertor to_uint error: val cannot be negative.", num)
    return num

def to_ufloat(val):
    num = float(val)
    if num < 0:
        raise Exception("convertor to_ufloat error: val cannot be negative.", num)
    return num

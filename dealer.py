# -*- coding: utf-8 -*
 
import json
import convertor 

class djson(object):
    def __init__(self, filename, title_row, type_row):
        self.filename = filename
        self.title_row = title_row
        self.type_row = type_row
        self.type_convertor = []

        def val_convertor(cname):
            switch = {
                'double': float,
                'float': float,
                'string': str,
                'str': str,
                'int': convertor.toint,
                'int8':  convertor.toint,
                'int16':  convertor.toint,
                'int32':  convertor.toint,
                'int64':  convertor.toint,
                'long':  convertor.toint,
                'bool': lambda x: x == True or x == '1' or (isinstance(x, str) and (x.lower() == 'true' or x.lower() == 'y')),# 1==True
            }
            return switch.get(cname.strip().lower(), lambda x: x)

        for ind in range(0, len(type_row)):
            self.type_convertor.append(val_convertor(type_row[ind]))
        self.clear()

    def clear(self):
        self.entries = {}

    def convert(self, entry, row, ind):
        val = self.type_convertor[ind](row[ind])
        if isinstance(entry, dict):
            entry[self.title_row[ind]] = val
        elif isinstance(entry, list):
            entry.append(val)
        else:
            print('├    convert type error %s ==> %s' % (row[ind], val))

    def read_line(self, row):
        if row[0] == "":
            return
        _id = self.type_convertor[0](row[0])
        _entry = {}
        _entry_stack = []
        for col in range(1, len(row)):
            col_title = self.title_row[col]
            col_type = self.type_row[col]
            if col_type == '{':
                _entry_stack.append(_entry)
                _entry[col_title] = {}
                _entry = _entry[col_title]
            elif col_type == '}':
                _entry = _entry_stack.pop()
            elif col_type == '[':
                _entry_stack.append(_entry)
                _entry[col_title] = []
                _entry = _entry[col_title]
            elif col_type == ']':
                _entry = _entry_stack.pop()
            else:
                self.convert(_entry, row, col)
        if len(_entry_stack) > 0:
            print("├    parse row(%d) error ==> object parser not close" % row)
        else:
            self.entries[_id] = _entry

    def print_entries(self):
        for x in self.entries:
            print(self.entries[x])

    def dump_json(self, indent=4):
        return json.dumps(self.entries, indent=indent)

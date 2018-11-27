# -*- coding: utf-8 -*

import xlrd
import os
import json
import codecs
import sys

INPUT_PATH = './_source'
OUTPUT_PATH = './_dist'
OVERRIDE = True

# file name log


def _log_file_operation(func):
    def executor(*args, **kw):
        print('┌─ executr file operation %s : %s' % (func.__name__, *args))
        ret = func(*args, **kw)
        if ret == False:
            print("└    not match")
        else:
            print("├    matched ==> %s" % ret)
        return ret
    return executor

# file name filter


@_log_file_operation
def excel_filename_filter(filename):
    if filename[0] == '_' or filename[0] == '~':
        return False
    else:
        return filename.strip()


def export_data(data, *route_path):
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    export_path = os.path.join(OUTPUT_PATH, *route_path)
    if os.path.exists(export_path) and not OVERRIDE:
        print("└    there is already an file : %s" % export_path)
    else:
        print("└    export data : %s" % export_path)
        with open(export_path, "w+") as f:
            f.write(data)


class json_dealer(object):
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
                'int': int,
                'int8': int,
                'int16': int,
                'int32': int,
                'int64': int,
                'long': int,
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


# procedure :
# read file
# create dealer
# dump dealer and export


dirs = os.listdir(INPUT_PATH)
for filename in dirs:
    filename = excel_filename_filter(filename)
    if not filename:
        continue

    wb = xlrd.open_workbook(os.path.join(INPUT_PATH, filename))

    entries = {}
    sh = wb.sheet_by_index(0)
    title = sh.row_values(2)
    datatype = sh.row_values(1)

    d = json_dealer(filename, title, datatype)
    for i_row in range(3, sh.nrows):
        row = sh.row_values(i_row)
        d.read_line(row)

    export_data(d.dump_json(), os.path.splitext(filename)[0] + ".json")

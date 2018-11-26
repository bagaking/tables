import xlrd
import os
from collections import OrderedDict
import json
import codecs
import sys


INPUT_PATH = './excel';
OUTPUT_PATH = './cfg';
OVERRIDE = True;

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
        with open(export_path ,"w+") as f:
            f.write(data)

class dealer(object):
    def __init__(self, filename, title_row, type_row):
        self.filename = filename
        self.title_row = title_row
        self.type_row = type_row
        self.type_convertor = [] 
        for ind in range(0, len(type_row)):
            self.type_convertor.append({
                'string': str,
                'str': str,
                'int': int,
            }.get(type_row[ind], lambda x: x))
        self.clear()

    def clear(self):
        self.convert_list = {}

    def convert(self, entry, row, ind):
        entry[self.title_row[ind]] = self.type_convertor[ind](row[ind])

    def read_line(self, row):
        if row[0] == "":
            return;
        _id = self.type_convertor[0](row[0])
        _entry = {}
        for col in range(1, len(row)):
            self.convert(_entry, row, col)
        self.convert_list[_id] = _entry

    def print_convert_list(self):
        for x in self.convert_list:
            print(self.convert_list[x])

    def dump_json(self, indent = 4):
        return json.dumps(self.convert_list, indent = indent)
        
dirs = os.listdir(INPUT_PATH)
for filename in dirs:
    filename = excel_filename_filter(filename)
    if not filename:
        continue

    wb = xlrd.open_workbook(os.path.join(INPUT_PATH, filename))

    convert_list = {}
    sh = wb.sheet_by_index(0)
    title = sh.row_values(2)
    datatype = sh.row_values(1)

    d = dealer(filename, title, datatype)
    for i_row in range(3, sh.nrows):
        row = sh.row_values(i_row)
        d.read_line(row)

    export_data(d.dump_json(), os.path.splitext(filename)[0] + ".json")


    

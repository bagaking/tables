# -*- coding: utf-8 -*

import sys
import os
import codecs
import xlrd

import dealer

INPUT_PATH = './_source'
OUTPUT_PATH = './_dist'
OVERRIDE = True

def _log_file_operation(func):
    def executor(*args, **kw):
        print('┌─ executr file operation %s : %s' % (func.__name__, args))
        ret = func(*args, **kw)
        if ret == False:
            print("└    not match")
        else:
            print("├    matched ==> %s" % ret)
        return ret
    return executor

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

dirs = os.listdir(INPUT_PATH)
for filename in dirs:
    filename = excel_filename_filter(filename)
    if not filename:
        continue

    # 1. read file
    wb = xlrd.open_workbook(os.path.join(INPUT_PATH, filename))

    entries = {}
    sh = wb.sheet_by_index(0)
    title = sh.row_values(2)
    datatype = sh.row_values(1)

    # 2. create dealer
    d = dealer.djson(filename, title, datatype)
    for i_row in range(3, sh.nrows):
        row = sh.row_values(i_row)
        d.read_line(row)

    # 3. dump dealer and export
    export_data(d.dump_json(), os.path.splitext(filename)[0] + ".json")

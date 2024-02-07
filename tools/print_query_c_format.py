#!/usr/bin/env python
#
import sys
import re

if len(sys.argv) != 2:
    print(f'''
    Reads file with SQL commands and outputs it formatted for C source code.
    Output is stdout.
    Usage:
    {sys.argv[0]} SQL_FILE
    ''')
    sys.exit(1)

filename = sys.argv[1]

indent = ' ' * 4

# C-Version
file_query = open(filename, "r")
for line in file_query:
    line_strip = line.rstrip()  # remove all \n \r space at the end
    print(indent + '" ' + line_strip, end='')
    if (re.search(r'\($', line_strip) or
        re.search(r'\);$', line_strip) or
        re.search(r'--', line_strip)):
        print('\\n"')
    else:
        print('"')
file_query.close()

# Python-Version
# print('    ' + line_strip + '\n', end='')

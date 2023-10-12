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

# C-Version
file_query = open(filename, "r")
for line in file_query:
    line_strip = line.rstrip()  # remove all \n \r space at the end
    # comment at the beginning of the line?
    if re.search(r'^/\*|\*\*|\*/', line_strip):
        print('  ' + line_strip + '\n', end='')
    else:
        print('  " ' + line_strip + '"' + '\n', end='')
file_query.close()

# Python-Version
# print('    ' + line_strip + '\n', end='')

#!/usr/bin/python
# Allows listing directories for mafuse
#
# Usage: list.py <afusetab> <root>
# afusetab: the file containing afuse paths and commands
# root: the root directory that was mounted by afuse


from __future__ import print_function
import sys
import os
import yaml
import re

#print(sys.argv)

if len(sys.argv)!=3:
    print("Wrong argument count. Usage: list.py <afusetab> <root>", file=sys.stderr)
    sys.exit(1)
elif not os.path.exists(sys.argv[1]):
    print("afusetab not found", file=sys.stderr)
    sys.exit(1)

try:
    with open(sys.argv[1],'r') as f:
        doc = yaml.load(f)
except:
    print("couldn't parse afusetab", file=sys.stderr)
    sys.exit(2)

afusemount=sys.argv[2]

try:
    rootnode = doc[afusemount]
except:
    print("afusemount combination not found", file=sys.stderr)
    sys.exit(3)

for child in rootnode: print(child)

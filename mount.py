#!/usr/bin/python
# unmount script for mafuse - managed afuse system
# usage: mafuse <afusetab> <afusemount> <directory>
# afusetab  : the file containing the afuse configuration
# afusemount: the directory where afuse was mounted (NOT the directory to be unmounted)
# directory : the directory to unmount

from __future__ import print_function
import sys
import os
import yaml

if len(sys.argv)!=4:
    print("Wrong argument count. usage: mafuse <afusetab> <afusemount> <directory>", file=sys.stderr)
    sys.exit(1)
elif not os.path.exists(sys.argv[1]):
    print("afusetab not found", file=sys.stderr)
    sys.exit(1)
# Now we can assume things are ok
with open(sys.argv[1],'r') as f:
    doc = yaml.load(f)

if doc is None:
    print("afusetab couldn't load", file=sys.stderr)
    sys.exit(2)

# find the right root, then the right directory
afusemount=sys.argv[2]
directory=sys.argv[3]
try:
    command = doc[afusemount][directory]['umount']
except:
    print("afusemount/directory combination umount command not found", file=sys.stderr)
    sys.exit(3)

print(command)
#import pprint
#pprint.pprint(doc)

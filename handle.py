#!/usr/bin/python
# mount / unmount script for mafuse - managed afuse system
# usage: handle.py <afusetab> <afusemount> <directory> <action>
# afusetab  : the file containing the afuse configuration
# afusemount: the directory where afuse was mounted (NOT the directory to be unmounted)
# subdirectory: the short name of the directory to mount / unmount (%r)
# directory : the fully qualified directory to mount / unmount (%m)
# action    : whether to mount or unmount. can be 'mount' or 'unmount'
# usage from afuse (as intended): ./handle.py <afusetab> <afusemount> %r %m {mount|unmount}

from __future__ import print_function
import sys
import os
import yaml
import re

print(sys.argv)

if len(sys.argv)!=6:
    print("Wrong argument count. usage: handle.py <afusetab> <afusemount> <directory> <action>", file=sys.stderr)
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

# find the right root, then the right directory
afusemount=sys.argv[2]
subdirectory=sys.argv[3]
directory=sys.argv[4]
directive=sys.argv[5]

# ignore .Trash bug in afuse / Ubuntu
if re.search("^\.Trash",subdirectory): exit(4)

try:
    command = doc[afusemount][subdirectory][directive]
except:
    print("afusemount/subdirectory/directive combination not found", file=sys.stderr)
    sys.exit(3)

command=command.replace('%r',afusemount)
command=command.replace('%m',directory)
print(command)

res = os.system(command)

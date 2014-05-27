#!/usr/bin/python
# mount / unmount script for mafuse - managed afuse system
# usage: handle.py <afusetab> <afusemount> <directory> <action>
# afusetab  : the file containing the afuse configuration
# afusemount: the directory where afuse was mounted (NOT the directory to be unmounted) (%r)
# directory : the fully qualified directory to mount / unmount (%m)
# action    : whether to mount or unmount. can be 'mount' or 'unmount'
# usage from afuse (as intended): ./handle.py <file> %r %m <mount/unmount>

from __future__ import print_function
import sys
import os
import yaml
import re

if len(sys.argv)!=5:
    print("Wrong argument count. usage: mount.py <afusetab> <afusemount> <directory> <action>", file=sys.stderr)
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
subdirectory=re.sub('^%s/' % re.escape(sys.argv[2]),'',sys.argv[3])
directive=sys.argv[4]
try:
    command = doc[afusemount][subdirectory][directive]
except:
    print("afusemount/subdirectory/directive combination not found", file=sys.stderr)
    sys.exit(3)

command=command.replace('%r',afusemount)
command=command.replace('%m',directory)
print(command)
#os.system(command)

#!/usr/bin/python
# Initializes afuse according to file
# usage: ./init.py [afusetab]
# afusetab: list of afuse mounts to init. If none are present, local file named afusetab is assumed.

from __future__ import print_function
import sys
import os
import yaml
import re
import argparse

parser = argparse.ArgumentParser(description='Initialize afuse according to a file')
parser.add_argument('afusetab',nargs='?',default='afusetab',help='Location of the afusetab file to parse')
parser.add_argument('-f','--foreground',help='run afuse in foreground (for troubleshooting)',action='store_true')
args = parser.parse_args()
'''
if len(sys.argv)>2:
    print("Wrong argument count. usage: handle.py [afusetab]", file=sys.stderr)
    sys.exit(1)
afusetab='afusetab'
if len(sys.argv)==2: afusetab=sys.argv[1]
if not os.path.exists(afusetab):
    print("afusetab not found", file=sys.stderr)
    sys.exit(1)
'''
'''
try:
    with open(afusetab,'r') as f:
        doc = yaml.load(f)
'''
afusetab = args.afusetab
try:
    with open(afusetab,'r') as f:
        doc = yaml.load(f)
except:
    print("couldn't prase afusetab", file=sys.stderr)
    sys.exit(2)

# script paths:
d = os.path.dirname(os.path.realpath(__file__))
handles="%s/handle.py" % (d)
lists="%s/list.py" % (d)

# convert afusetab to fully qualified location
afusetab=os.path.realpath(afusetab)

# find all roots in the document, and for every one of those invoke a proper command
for root in doc:
    mounttemplate='mount_template=%s %s %s %%r %%m mount' % (handles,afusetab,root)
    unmounttemplate='unmount_template=%s %s %s %%r %%m unmount' % (handles,afusetab,root)
    poproottemplate='populate_root_command=%s %s %s' % (lists,afusetab,root)
    callarr = ['afuse','-o',mounttemplate,'-o',unmounttemplate,'-o',poproottemplate,root]
    if(args.foreground): callarr.append('-f')
    from subprocess import call
    call(callarr)

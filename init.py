#!/usr/bin/env python2

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
parser.add_argument('afusetab',nargs='?',default=None,help='Location of the afusetab file to parse. Defaults to "afusetab" located near script')
parser.add_argument('-f','--foreground',help='run afuse in foreground (for troubleshooting)',action='store_true')
args = parser.parse_args()

afusetab = args.afusetab
if afusetab is None:
    afusetab = os.path.join(os.path.dirname(__file__),'afusetab')
try:
    with open(afusetab,'r') as f:
        doc = yaml.load(f)
except:
    raise Exception("couldn't prase afusetab. Make sure it exists and valid")
    #print("couldn't prase afusetab. Make sure it exists and valid", file=sys.stderr)
    #sys.exit(2)

# script paths:
d = os.path.dirname(os.path.abspath(__file__))
handles="%s/handle.py" % (d)
lists="%s/list.py" % (d)

# convert afusetab to fully qualified location
afusetab=os.path.abspath(os.path.expanduser(afusetab))


# find all roots in the document, and for every one of those invoke a proper command
for root in doc:
    realroot=os.path.abspath(os.path.expanduser(root))
    mounttemplate='mount_template=%s %s %s %%r %%m mount' % (handles,afusetab,root)
    unmounttemplate='unmount_template=%s %s %s %%r %%m unmount' % (handles,afusetab,root)
    poproottemplate='populate_root_command=%s %s \'%s\'' % (lists,afusetab,root)
    callarr = ['afuse','-o','nonempty','-o',mounttemplate,'-o',unmounttemplate,'-o',poproottemplate,realroot]
    if(args.foreground): callarr.append('-f')
    from subprocess import call
    call(callarr)

#!/usr/bin/python
# encoding: utf-8
""" Just something to slurp up a json object and spit out something more
    sorted.  Useful for keeing vocabulary files organized, and to find
    duplicate data in vocabulary files.
"""

import json, sys
if len(sys.argv) <= 1 :
  print "Usage: %s file.json >file.sorted.json" % (sys.argv[0])
  sys.exit(1)

FH = open(sys.argv[1], 'r')
THING = json.load(FH)
for i in THING :
  if isinstance(THING[i], (list, tuple)):
    SORTED = list(THING[i])
    SORTED.sort()
    THING[i] = SORTED

json.dump(THING, sys.stdout, check_circular=False, indent=2, sort_keys=True)


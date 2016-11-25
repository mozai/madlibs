#!/usr/bin/python3
# encoding: utf-8
""" Just something to slurp up a json object and spit out something more
    sorted.  Useful for keeing vocabulary files organized, and to find
    duplicate data in vocabulary files.
"""
import json
import sys

if len(sys.argv) <= 1:
  print("Usage: %s file.json >file.sorted.json" % (sys.argv[0]))
  sys.exit(1)

FH = open(sys.argv[1], 'r')
THING = json.load(FH)
THINGKEYS = sorted(THING.keys())
for i in THINGKEYS:
  if i == '#':
    THING[i] = str(THING[i])
  elif isinstance(THING[i], str):
    THING[i] = [THING[i], ]
  elif isinstance(THING[i], list):
    THING[i].sort()
  else:
    raise ValueError("term %s has illegal value type %s" % (i, repr(type(THING[i]))))

# for each item on its own line
# json.dump(THING, sys.stdout, check_circular=False, indent=2, sort_keys=True)

# for more than one item on each line, with word-wrap that doesn't
# insert '\n' in the middle of strings
LINELENGTH = 78
LINE = ''
for NEXTLINE in json.dumps(THING, check_circular=False, indent=2, sort_keys=True).split("\n"):
  NEXTLINESTRIPPED = NEXTLINE.strip()
  if NEXTLINESTRIPPED in ('{', '}', ']', '],') or NEXTLINESTRIPPED[:4] == '"#":':
    if LINE.strip():
      print(LINE)
    print(NEXTLINE)
    LINE = ''
  elif NEXTLINESTRIPPED[-1] == '[':
    if LINE.strip():
      print(LINE)
    print(NEXTLINE)
    LINE = '   '
  else:
    if (len(LINE) + 1 + len(NEXTLINESTRIPPED)) < LINELENGTH:
      LINE += " " + NEXTLINESTRIPPED
    else:
      if LINE.strip():
        print(LINE)
      LINE = NEXTLINE.rstrip()

#!/usr/bin/python3
" emit just one madlib "
# TODO compiled version of this
import madlibs
import sys

VFILE = None
HOWMANY = 0
if (len(sys.argv) == 2):
    VFILE = sys.argv[1]
    HOWMANY = 1
elif (len(sys.argv) == 3):
    VFILE = sys.argv[1]
    HOWMANY = int(sys.argv[2])
if (not VFILE or not HOWMANY):
    print(f"Usage: {sys.argv[0]} vocabulary.json [howmany]")
    sys.exit(1)
ML = madlibs.Madlibs(VFILE)
if not ML.load(VFILE):
    print(f"{VFILE} did not load.")
    sys.exit(1)
for i in range(HOWMANY):
    print(ML.story())

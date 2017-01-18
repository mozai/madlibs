#!/usr/bin/python3
" for testing vocabulary files "

import madlibs
import sys

if (len(sys.argv) <= 1):
  print('Usage: %s vocabulary.json' % sys.argv[0])
  sys.exit(1)

VFILE = sys.argv[1]
ML = madlibs.Madlibs(VFILE)
if not ML.load(VFILE):
  print(VFILE + "did not load.")
  sys.exit(1)
print("{} loaded; {} stories.".format(VFILE, len(ML)))

print("validating vocabulary...")

if not ML.validate():
  print("did not pass validate")
  print("\n".join(ML.errors))
  sys.exit(1)

if ML.warnings:
  print("warnings")
  print("\n".join(ML.warnings))

print("testing story generation")
for i in range(3 * len(ML)):
  ML.story()

print("seems okay; here's five samples")
for i in range(5):
  print("- " + ML.story())

#!/usr/bin/python
" for testing vocabulary files "

import madlibs, sys

if (len(sys.argv) <= 1):
  print 'Usage: %s vocabulary.json' % sys.argv[0]
  sys.exit(1)

VFILE = sys.argv[1]
ML = madlibs.Madlibs(VFILE)
if not ML.load(VFILE):
  print VFILE, "did not load."
  sys.exit(1)
print VFILE, "loaded;", len(ML), "stories."

print "validating vocabulary..."

if not ML.validate():
  print "\n".join(ML.errors)
  sys.exit(1)

if ML.warnings:
  print "\n".join(ML.warnings)

for i in range(3*len(ML)):
  ML.story()

print "(seems okay; here's five samples)"
for i in range(5):
  print ML.story()


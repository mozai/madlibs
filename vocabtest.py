#!/usr/bin/python
#
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
REPORT = ML.validate()
if not REPORT == '' :
  print REPORT
  sys.exit(1)
for I in range(3*len(ML)):
  STORY = ML.story()
  if STORY.find('%') >= 0 :
    print "badstory\n ", STORY
print "---"
print ML.story()
print "---"
print "Done."


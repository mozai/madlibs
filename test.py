#!/usr/bin/python
#
""" test suite for madlibs.Madlibs
    Moses Moore, 20120929
"""
import madlibs, sys
VFILE = 'test.json'

print("testing madlibs.py with", VFILE)
ML = madlibs.Madlibs(VFILE)
if not ML.load(VFILE):
  print VFILE , "did not load."
  sys.exit(1)
  
print VFILE , " loaded; " , len(ML) , "stories."
print '' 

print "validating vocabulary..."
REPORT = ML.validate()
if REPORT == '':
  print "no problems; forgot to put a bad term in there, boss?"
  sys.exit(1)
else:
  print "found your bait boss; make sure it's the correct bad stuff"
  print REPORT
print ''

print "test run of 2x the stories in" , VFILE
for I in range(2*len(ML)):
  print "..." , ML.story()
print ''


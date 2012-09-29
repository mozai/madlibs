Madlibs module for Python
=========================

The idea: class that you instantiate with a vocabulary dict().
Ask the instance for a random story, it selects a random story-template
from its vocabulary, substituting marked spots with appropriate
random words from elsewhere in its vocabulary.

Example:
    "It sure is %(sunny|wet|hot|cold|awful) here in %city."

The first marked area `%(sunny|wet|hot|cold|awful)` will choose one
of the items seperated by '|' marks.  The second marked area `%city`
will use a 'city' list defined elsewhere in the vocabulary.

Here is an example vocabulary dict():

    {
      "@": ["weather"], # a list of story types in this vocabulary
      "city": [ "Cincinati", "Montreal", "London" ]
      "weather": [
        "It sure is %(sunny|wet|hot|cold|awful) here in %city.",
        "It rains %(often|not at all) in %city.",
        "Having a wonderful time in %city, wish you were here."
      ]
    }

The names of the lists the vocabulary are called *terms*.  In
the example above, `%city` marks an area that will be replaced
with a random item from the 'city' list.

**Terms** in the vocabulary must start with an alpha char (A-Za-z) 
and have only characters in the set (A-Za-z0-9.\_)  *('.' will have a
special meaning later, but it will be backwards compatible)*  Terms
that are a single character from the set (!@#$%^&\*) are reserved for
internal use.  The '@' term is used for identifying term used for 
stories, so that a vocabulary can have many stories and can be asked
for a random one, instead of being provided a story string to 
mix up.  The '#' term is used for comments about the vocabulary itself,
such as author, citing sources, intended use, and so on.

**Values** are the items in a term's list.  Values are strings or unicode
strings *(for now)*.  When a term is requested from a madlibs object
exactly one value will be returned, and it (hopefully) will not be the 
same value as the previous request for that term.  Values may also
contain %(a|b|c) or %abc marked areas, which will be replaced with
appropriate values before being returned to the requester.  Loops
are possible, but if a loop goes on too often an exception will be raised.

A vocabulary is usually loaded from a text file at creation time,
or with the madlibs.load() method.  You can provide a filename
or a file-like object:

    ML = madlibs.Madlibs('filename.json')

    ML = madlibs.Madlibs()
    ML.load('filename.json')
    ML.load(shelve.open('vocab.db'))

The current version expects the file to be a JSON dictionary/ hash/
mapping object.  You can also provide a dict() object, which permits
use of the Python module 'shelve' for persistence.

---
TODO: verb congutates.   
  %move.2 -> "move":[["run","ran","running"],] -> "running"  
TODO: more dict()-like methods to make it python paradigm friendly.  
TODO: escape \| in %() : i.e.: %(alpha\|a|beta\|b|gamma\|c)   
TODO: recommended limits for terms; see if keeping lists under 255 values
  if it matters, or value strings under 4096 bytes (python voodo?)
TODO: is the '%%' escaping efficient enough? would \% be better?
TODO: problems with unicode chars in \*.json file: "UnicodeEncodeError: 'ascii' codec can't encode character u'\u32e1' in position 0: ordinal not in range(128)"

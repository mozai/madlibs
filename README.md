Madlibs module for Python
=========================

The idea: class that you instantiate with a vocabulary dict(). Ask 
the instance for a random story, it selects a random story-template 
from its vocabulary, substituting marked spots with appropriate 
random words from elsewhere in its vocabulary.


Example Vocabulary
------------------
    "It sure is %(sunny|wet|hot|cold|awful) here in %city."

The first marked area `%(sunny|wet|hot|cold|awful)` will choose one 
of the items seperated by '|' marks.  The second marked area `%city` 
will use a 'city' list defined elsewhere in the vocabulary.

Here is an example vocabulary dict():

    {
      "@": ["weather"],
      "city": [ "Cincinati", "Montreal", "London" ]
      "weather": [
        "It sure is %(sunny|wet|hot|cold|awful) here in %city.",
        "It rains %(often|not at all) in %city.",
        "Having a wonderful time in %city, wish you were here."
      ]
    }

The names of the lists the vocabulary are called *terms*.  In the 
example above, `%city` marks an area that will be replaced with a 
random item from the 'city' list.

Here is example code that would use the above vocabulary:

    import madlibs
    ML = madlibs.Madlibs('example.json')
    print ML.story()


Terms and Values
----------------
Terms and Values correspond to the key/value pairs of a dict(),
with some extra rules for how they are to be used.

**Terms** in the vocabulary must start with an alpha char (A-Za-z) 
and have only characters in the set (A-Za-z0-9.\_)  *('.' will have a
special meaning later, but it will be backwards compatible)*  Terms 
that are a single character from the set (!@#$%^&\*) are reserved 
for internal use.  

Of the reserved Terms, two are currently used:

- The '@' Term is used for identifying Term used to start stories, so 
  that a vocabulary can have many stories and can be asked for a 
  random one, instead of being provided a story string to mix up.
  Each vocabulary **must** have a valid '@' Term. 
- The '#' Term is used for comments about the vocabulary itself, 
  such as author, citing sources, intended use, and so on.  A
  vocabulary doesn't need to have a '#' Term, but it's recommended.

**Values** are the items in a term's list.  Values are strings or 
unicode strings.  When a term is requested from a madlibs object 
exactly one value will be returned.  If a Term has more than one 
Value, all possible Values will be used before repeating.

Values may also contain %(a|b|c) or %abc marked areas; 
the former will be a choice of replacedments for that area, the 
latter will be checked to see if it is a Term, and replaced with a 
value from that Term, otherwise left alone. A value from a such a 
Term may contain other markers, bringing in other values; loops are 
possible, but if a loop goes on too often an exception will be raised.


Loading A Vocabulary
--------------------
A vocabulary is usually loaded from a text file at creation time,
or with the madlibs.load() method.  You can provide a filename
or a file-like object:

    ML = madlibs.Madlibs('filename.json')
    ML.load(shelve.open('vocab.db'))

    ML = madlibs.Madlibs()
    ML.load('filename.json')
    ML.load(shelve.open('vocab.db'))

The current version expects the file to be a valid JSON dict(). You 
can also provide any other dict() object that obeys the rules for a 
valid vocabulary, which permits use of the Python module 'shelve' 
or other methods for persistence.


To-Do List
----------
- verb congutaton. Present, Past, Continuous, Perfect.
  i.e.: I do, I did, I am doing, I have done.
  i.e.: `I am %move.2` with `"move":[["run","ran","running","run"],]`
  becomes "I am running"
- more dict()-like methods to make it python paradigm friendly.
- investigate using string.Template instead of rolling my own.
- escape \| in %() : i.e.: `%(alpha\|a|beta\|b|gamma\|c)`
- recommended limits for Terms; see if keeping len(list()) under 255
  matters, or len(str()) under 4096

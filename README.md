Madlibs module for Python
=========================

The idea: class that you instantiate with a vocabulary dict().
Ask the instance for a random story, it selects a random story-template
from its vocabulary, substituting marked spots with appropriate
random words from elsewhere in its vocabulary.

Example:
    "It sure is |sunny,wet,hot,cold,awful| here in |n.city|."

The first marked area `|sunny,wet,hot,cold,awful|` will choose one
of the items seperated by ',' marks.  The second marked area `|n.city|`
will use a 'n.city' list defined elsewhere in the vocabulary.

Here is an example vocabulary dict():

    {
      "@": ["weather"], # a list of story types in this vocabulary
      "n.city": [ "Cincinati", "Montreal", "London" ]
      "weather": [
        "It sure is |sunny,wet,hot,cold,awful| here in |n.city|.",
        "It rains |often,not at all| in |n.city|.",
        "Having a wonderful time in |n.city|, wish you were here."
      ]
    }

Vocabulary items must be more than one character; single-character
items are reserved for internal use.  The item '@' is used for
identifying items used for stories, so that the madlibs instance
can be asked for a random story among all types it has.

Vocabulary items may contain "|marks|" but the vocabulary builder
must be careful not to allow loops.  If the madlibs instance
loops too often, it will throw an exception.

Some vocabulary items can be populated with lists; this is used
for (third-person) verb tenses as follows: present, past and
present-imperfect.  (this method is incomplete, and may change 
in the future; for now, using |verb,verb,verb| in your story
items is safest)

    "v.jump": [ ["leaps","leaped","leaping"], ["launches ]

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


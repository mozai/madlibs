Madlibs lib(rary)
=================
Stuff I've collected.  Few are original works, some are derived from
clunkier/ abandoned/ deleted madlibs software, some from pen-and-paper
charts.

Where possible, I credit the original authors in the "#" (comment)
element of the vocabulary file.


Example Vocabulary
------------------
    "It sure is %(sunny|wet|hot|cold|awful) here in %city."

The first marked area `%(sunny|wet|hot|cold|awful)` will choose one
of the items seperated by '|' marks.  The second marked area `%city`
will use a 'city' list defined elsewhere in the vocabulary.

Here is an example vocabulary dict():

    { "#": "This term is not used it is only comments",
      "@": [
        "It sure is %(sunny|wet|hot|cold|awful) here in %city.",
        "It rains %(often|not at all) in %city.",
        "Having a wonderful time in %city, wish you were here."
      ]
      "city": [ "Cincinati", "Montreal", "London" ]
    }

The names of the lists the vocabulary are called *terms*.  In the
example above, `%city` marks an area that will be replaced with a
random item from the 'city' list.


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

- The '@' Term is used for starting stories, either one string
  or a list of strings, that are the default if you don't pass
  a parameter to .story().
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


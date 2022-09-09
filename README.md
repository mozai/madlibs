Madlibs
=========================
The idea: simple-ish data structures generating random stories.
Like the parlour game "madlibs," there are templates with empty spaces
to substitue appropriate random words from lists.

Stuff that is "push button get new text" is in the bin/ subdir.  
Vocabulary files are in the libs/ subdir.

See [libs/README.md](libs/README.md) for how to write vocabulary files.


To-Do List
----------
- Vocabulary format
  - verb congutaton. Present, Past, Continuous, Perfect.
    i.e.: I do, I did, I am doing, I have done.
    i.e.: `I am %move.2` with `"move":[["run","ran","running","run"],]`
    becomes "I am running"
  - escape \| in %() : i.e.: `%(alpha\|a|beta\|b|gamma\|c)`
  - some inline memory; re-use a noun I chose earlier in the same story
  - recommended limits for Terms; see if keeping len(list()) under 255
    matters, or len(str()) under 4096
  - some call-response feature; use special term '$' ? ordered list of
    (regex1, term1) tuples.  Given message, iterate through '$' to find
    first tuple with matching regex, return .story(term1)
- General
  - improve modifiying the vocabulary at runtime and persisting changes.
  - some compiled language.  Go is popular but heavyweight. Ada?
- Javascript
  - demo page, like what I used for my writing practice blog
  - drop-in library for any HTML5 page
- Python
  - more dict()-like methods to make it python paradigm friendly.
  - investigate using string.Template instead of rolling my own.
- Lua
  - I wish you good luck


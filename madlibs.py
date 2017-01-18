# madlibs.py
# encoding: utf8
# author: Mozai <moc.iazom@sesom>
""" Madlibs takes a dict as vocabulary of story-strings with marked spots
for substituting random words or phrases from collections.   It is
intended to be used iteratively, and uses a randomizing method
intended for high novelty in the output.
God this description is poor; look for a readme.txt with this.  Especially
for how to make the vocabulary data-sets used to initialize this.
"""
# I'm taking the slow road to writing context-free grammars, aren't I?

import json
import random
# why am I avoiding using 're' ?
__version__ = '20161214'
# 20161124 : converting to Python3.
#   took out 'shelve' because I never used it
# 20161201 : slowing adding chatbot features, special term '$'
# 20161214 : adding mutators -- %{s:food} & food:(apple, candy) could
#            become "apples" or "candies"

# FIXME: '%{ab}s' with {'ab':['%cd']} becomes '%cds' and an error
# wanted: backref "An %bodyPart for an %{\1} makes the whole world blind."
#         maybe as a mutator? "%{set1:bodyPart} for an %{1}" ???
# thinking: Would it be better to subclass UserDict ?

BRACEPAIRS = (('(', ')'), ('[', ']'), ('{', '}'), ('<', '>'))
TERMCHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789:_'
RESERVEDTERMS = '!@#$%^&*:'
MUTATORS = { }  # append as they're defined, below

def _next_term_ij(data):
  # find %blah or %(blah) in string data; returns (i,j) to be used as s[i:j]"
  # returns (-1, -1) when not found
  # used repeatedly in Madlibs.get()
  # turns out nested parens is one of the medium-hard problems of compsci
  i = 0  # guess at left edge of term
  j = len(data)  # rightmost limit for a useful '%'
  found = (-1, -1)
  while i >= 0:
    i = data.rfind('%', None, j)
    if (i < 0):
      break
    if (i == j - 1) or (i != 0 and data[i - 1] == '%'):
      # "shown at 72%" or "%%terms like this"
      j = i - 1
      continue
    lbrace, rbrace = None, None
    for bracepair in BRACEPAIRS:
      if data[i + 1] == bracepair[0]:
        lbrace, rbrace = bracepair[0], bracepair[1]
    if lbrace is None:
      # either "with 37% share" or "eat %noun quickly"
      j = i + 1
      while (j < len(data)) and (data[j] in TERMCHARS):
        j += 1
      if j == i + 1:
        j = i
        continue
      else:
        found = (i, j)
        break
    else:
      # "eat the %{noun} quickly"
      j = data.find(rbrace, i)
      if j < 0:
        j = i
        continue
      else:
        found = (i, j + 1)
        break
  return found


def _unbrace(term):
  # "%{alpha}" becomes "alpha", "%beta" becomes "beta"
  # TODO: what of %{alpha|beta} ?
  if not term.startswith('%'):
    raise VocabularyError("trying to unbrace non-term \"{}\"".format(term))
  if (term[1], term[-1]) in BRACEPAIRS:
    term = term[2:-1]
  else:
    term = term[1:]
  return term


def _mutator_a(noun):
  # "apple" becomes "an apple"
  if noun[0] in 'aeiou':
    return 'an ' + noun
  else:
    return 'a ' + noun
MUTATORS['a'] = _mutator_a


def _mutator_s(noun):
  # "candy" becomes "candies"
  if noun[-1] == 's':
    return noun + 'es'
  elif noun[-1] == 'y':
    return noun[:-1] + 'ies'
  else:
    return noun + 's'
MUTATORS['s'] = _mutator_s


def _good_term(termname):
  # validate a term name
  # I'm trying to avoid importing re
  if not isinstance(termname, str):
    return False
  if ':' in termname:
    mutator, termname = termname.split(':', 1)
    if mutator not in MUTATORS:
      return False
  if not termname[0].isalpha():
    return False
  if '|' in termname:
    # it's valid, but not itself a vocabulary term
    return False
  if [i for i in termname if i not in TERMCHARS]:
    return False
  return True


def _extract_terms(data):
  # "%alpha is a %beta with a %{big|huge} %gamma" -> ['alpha', 'beta', 'gamma']
  terms = []
  (i, j) = (0, 0)
  (i, j) = _next_term_ij(data)
  while (i, j) != (-1, -1):
    term = _unbrace(data[i:j])
    if _good_term(term):
      terms.append(term)
    data = data[:i] + data[j+1:]
    (i, j) = _next_term_ij(data)
  return terms


class Madlibs(object):
  """ Each instance of this class will have its own vocabulary of stories.
  Using it without a vocabulary initialized will return 'None' or
  raise a KeyError if you try to request something specific from the
  vocabulary.
  Be ready to catch madlibs.VocabularyError or TypeError or KeyError
  """

  def __init__(self, vocabulary=None):
    " can pass a dict for vocabulary or filename to a vocabulary file "
    self.vocabulary = {'#': '', '@': ''}
    self.shuffles = {}
    self.errors = []
    self.warnings = []
    self.__contains__ = self.vocabulary.__contains__
    self.__eq__ = self.vocabulary.__eq__
    self.__iter__ = self.vocabulary.__iter__
    self.__lt__ = self.vocabulary.__lt__
    if vocabulary:
      self.load(vocabulary)

  def __del__(self):
    # if we were using a shelve, or pickle, or database
    # this is where we'd close filehandles safely
    NotImplemented

  def _is_valid(self):
    """ quick check of self.vocabulary for correctness of structure
    raises VocabularyError. use validate() method for diagnosing
    problems inside the data
    """
    self.errors = []
    if not isinstance(self.vocabulary, (dict)):
      self.errors.append('vocabulary is not a dict "%s"' % type(self.vocabulary))
    if '@' not in self.vocabulary:
      self.errors.append('term "@" is missing')
    if len(self.vocabulary['@']) == 0:
      self.errors.append('term "@" is empty')
    if not isinstance(self.vocabulary.get('#', ''), str):
      self.errors.append('term "#" is not a string')
    if '$' in self.vocabulary:
      if isinstance(self.vocabulary['$'], list):
        for i in self.vocabulary['$']:
          if (not isinstance(i, list)) or (len(i) < 2) or [j for j in i if not isinstance(j, str)]:
            self.errors.append('improper item in "$": ' + repr(i))
      else:
        self.errors.append('term "$" is not a list')
    for term in self.vocabulary.keys():
      if term in RESERVEDTERMS:
        pass
      elif not isinstance(self.vocabulary[term], (str, list)):
        self.errors.append('term %s is type %s' % (term, type(self.vocabulary[term])))
      elif not _good_term(term):
        self.errors.append('term "%s" is illegal' % term)
    if self.errors:
      raise VocabularyError("There were problems:\n" + "\n".join(self.errors))
    return True

  def delterm(self, term):
    " for removing a term from the vocabulary "
    del self.vocabulary[term]

  def __delitem__(self, term):
    " see delterm(t) "
    # shut UP pylint; I define it in __init__()
    return self.vocabulary.__delitem__(term)

  def load(self, filenameordict):
    """ reads a vocabulary data set from filename or a dict object
    could raise exceptions from file.open() or json.load()
    raises VocabularyError if improper structure.
    """
    self.vocabulary = None
    if isinstance(filenameordict, (dict)):
      self.vocabulary = filenameordict
    elif isinstance(filenameordict, str):
      infile = open(filenameordict, 'r')
      self.vocabulary = json.load(infile)
      infile.close()
    else:
      raise TypeError("expecting filename or dict")
    if self.vocabulary:
      self.__iter__ = self.vocabulary.__iter__
      self.__contains__ = self.vocabulary.__contains__
    return self._is_valid()

  def sync(self):
    # if we were using a shelve, or pickle, or database
    # this is where we'd flush buffers
    NotImplemented

  def save(self, filething):
    " saves the vocabulary state to file or file-object "
    if isinstance(filething, str):
      filething = open(filething, 'w')
    if hasattr(filething, 'read'):  # can't isinstance(f, file) in Python3
      json.dump(self.vocabulary, filething, sort_keys=True, indent=2)
      filething.close()
    else:
      raise TypeError("expected str or file object; received " + type(filething))

  def validate(self):
    """ checks the vocabulary for problems
    returns False if problems are found ("valid == False")
    and populates self.errors and self.warnings as a list
    """
    # "too many branches (20/12)"  shut up, pylint
    self.errors = []    # side effects! hisssss!
    self.warnings = []  # side effects! hisssss!
    try:
      self._is_valid()
    except VocabularyError:
      # we might have more errors to pile on
      pass
    terms = list(self.vocabulary.keys())
    terms.sort()
    termsseen = set()
    # if we're going to have term '$' for call-response,
    #   we'll need extra validation
    for term in terms:
      try:
        if (term != '@') and (term in RESERVEDTERMS):
          # already checked with self._is_valid()
          pass
        else:
          # term
          values = self.vocabulary[term]
          if isinstance(values, str):
            values = [values, ]
          if not isinstance(values, list):
            self.errors.append('term %s has unexpected value type "%s"' % (term, type(values)))
          elif len(values) == 0:
            self.errors.append('term "%s" has zero values' % term)
          else:
            for value in values:
              foundterms = _extract_terms(value)
              termsseen.update(foundterms)
              try:
                for termtolookup in foundterms:
                  termtolookup = termtolookup[termtolookup.find(':')+1:]
                  if termtolookup not in self.vocabulary:
                    self.errors.append('term "%s" has unknown term "%s" in value "%s"' % (term, termtolookup, value))
              except Exception as err:
                self.errors.append('term "%s" has troublesome value "%s"; (%s)' % (term, str(value), str(err)))
      except Exception as err:
        self.errors.append('term "%s": %s' % (term, repr(err)))
        raise
    for term in terms:
      if len(term) > 1 and term not in termsseen:
        self.warnings.append('term "%s" is unused' % term)
    return len(self.errors) == 0

  def addterm(self, term, data=None):
    " for adding a new term to the vocabulary "
    if term in self:
      self.insert(term, data)
    elif not _good_term(term):
      raise TypeError('bad term; "%s"' % type(term))
    elif data is None:
      self.vocabulary[term] = []
    elif isinstance(data, str):
      self.vocabulary[term] = [data]
    elif isinstance(data, list):
      self.vocabulary[term] = list(data)
    else:
      raise TypeError('bad data; expected str or list; received ' + type(data))

  def insert(self, term, data=None):
    " for adding more values to a term in the vocabulary "
    if not isinstance(term, str):
      raise TypeError('bad term; expected str, got ' + type(term))
    if term not in self.vocabulary:
      self.addterm(term, data)
    elif isinstance(data, str):
      self.vocabulary[term].append(data)
    elif isinstance(data, list):
      # "why temp?" just in case self.vocabulary is shelve.Shelf
      temp = self.vocabulary[term]
      for i in data:
        temp.append(i)
      self.vocabulary[term] = temp
    else:
      raise TypeError('bad data; expected str or list, got ' + type(data))

  def __setitem__(self, term, data):
    "see insert()"
    self.insert(term, data)

  def remove(self, term, data):
    """ removes an item from a term
    The entire item must be included with marks intact and case-sensitive
    If the item isn't associated with this term, it will return False.
    """
    if term not in self.vocabulary:
      raise KeyError('term not found in vocabulary; ' + term)
    try:
      self.vocabulary[term].remove(data)
    except ValueError:
      return False
    return True

  def __len__(self):
    """how many random stories are available in the loaded vocabulary.
    This is not the same as how many terms are in the vocabulary.
    """
    if len(self.vocabulary) == 0:
      return None
    if '@' not in self.vocabulary:
      return 0
    if isinstance(self.vocabulary['@'], str):
      return 1
    return len(self.vocabulary['@'])

  def __getitem__(self, term):
    "see get()"
    return self.get(term)

  def get(self, term, default=None):
    """ returns a random item from that term in the vocabulary
    for convenience, given '(alpha|beta|gamma)' it will return
    a random choice from 'alpha' or 'beta' or 'gamma'
    single-character term is not allowed; will raise KeyError
    """
    if not isinstance(term, str):
      raise TypeError('bad term type ' + repr(type(term)))
    if term[0] == '%':
      # in case we passed %fruit instead of 'fruit'
      term = term[1:]
    if not term:
      # we were passed '%' or ''; eye-dee-ten-tee issue
      return default
    if (term[0], term[-1]) in BRACEPAIRS:
      term = term[1:-1]

    if '|' in term:
      # it's %(alpha|beta|gamma) type
      values = term.split('|')
    else:
      # else it's %fruitcolour type
      key = term
      values = self.vocabulary.get(key)
      while values is None and '.' in key:
        key = key[:key.rindex('.')]
        values = self.vocabulary.get(key)
      if isinstance(values, str):
        values = [values, ]

    value = default
    if values:
      if not self.shuffles.get(term):
        self.shuffles[term] = list(range(len(values)))
        random.shuffle(self.shuffles[term])
      value = values[self.shuffles[term].pop()]

    return value

  def comments(self, data=None):
    " get/set comment text for the vocabulary "
    if data is None:
      return self.vocabulary.get('#')
    else:
      self.vocabulary['#'] = str(data)

#  def templates(self, termlist=None):
#    """ get/set which terms in the vocabulary are story templates
#    terms provided must already exist in the vocabulary
#    """
#    if termlist == None :
#      return self.vocabulary['@']
#    elif isinstance(termlist, str):
#      if not termlist in self.vocabulary:
#        raise KeyError('bad template list; "'+termlist+'" not found in vocabulary')
#      self.vocabulary['@'] = [termlist,]
#    elif isinstance(termlist, list):
#      for i in termlist:
#        if not i in self.vocabulary:
#          raise KeyError('bad template list; "'+i+'" not found in vocabulary')
#      self.vocabulary['@'] = termlist
#    else:
#      raise ValueError('improper type "%s" for termlist' % type(termlist))
#
#  def get_template(self, term=None, search=None):
#    """ fetches a random template from the vocabulary.
#    term: use this term; can be a list of terms
#    search: only choose from the stories that have this substring
#    """
#    if self.vocabulary == None :
#      return None
#    if not '@' in self.vocabulary :
#      raise VocabularyError("missing '@' term in vocabulary")
#    if isinstance(term, str) :
#      template_types = [term,]
#    elif isinstance(term, list) :
#      template_types = list(term)
#    else:
#      template_types = self.vocabulary['@']
#    if search :
#      stories = []
#      for i in template_types:
#        for j in self.vocabulary[i]:
#          if j.find(search) >= 0 :
#            stories.append(j)
#      if len(stories) == 0:
#        # no matches among the template_types we're supposed to use
#        return None
#      else:
#        return random.choice(stories)
#    else:
#      return self.get(random.choice(template_types))

  def story(self, template=None):
    """ in template, replaces all the %(word1|word2|word3) with a
    random item and replaces %keyname with a random item from the
    vocab if template not provided, gets a new one from get_template()
    """
    if template is None:
      #template = self.get_template()
      template = self.get('@')
    text = template
    bad_loop = []
    (i, j) = _next_term_ij(text)
    old_i = i
    old_j = j
    while i >= 0 and j > 0:
      term = _unbrace(text[i:j])
      try:
        term = self.get(term)
      except KeyError as err:
        raise VocabularyError('bad template "%s"; (%s)' % (template, str(err)))
      if term is not None:
        text = text[:i] + term + text[j:]
        (i, j) = _next_term_ij(text)
      else:
        (i, j) = _next_term_ij(text)
      if j > 0 and j <= old_j:
        bad_loop.append(term)
        if len(bad_loop) > 5:
          raise VocabularyError('vocabulary loop detected ' + repr(bad_loop) + ' in \"' + template + '\"')
      else:
        bad_loop = []
      old_j = j
    text = text.replace('%%', '%')  # unescape the doubled percents
    return text


class VocabularyError(Exception):
  """ For errors caused by misunderstanding the internal structure
  of the Madlibs vocabulary data; missing values, trying to add
  non-strings as terms, and so on.  Easier to catch this way.
  """

# madlibs.py
# encoding: utf8
# author: Mozai <moc.iazom@sesom>
# version: 20121213
""" Madlibs takes a dict as vocabulary of story-strings with marked spots
for substituting random words or phrases from collections.   It is
intended to be used iteratively, and uses a randomizing method
intended for high novelty in the output.
God this description is poor; look for a readme.txt with this.  Especially
for how to make   the vocabulary data-sets used to initialize this.
"""
import json, random, shelve
import anydbm # only so I can catch anydbm.error

# TODO: if 'ab':['%cd'], then '%ab' -> '%cd' -> 'CD', but '%{ab}s' -> '%cds' -> error
# wanted: backref "An %bodyPart for an %{\1} makes the whole world blind."
# test: 'alpha.bet' is a valid term, decays to 'alpha' if 'alpha.bet' empty.
# thinking: Would it be better to subclass UserDict ?

# used for on-the-fly terms in stories. ie: %{red|cerulian|rust|cherry}
BRACEPAIRS = (('(', ')'), ('[', ']'), ('{', '}'), ('<', '>'), ('|', '|'))
TERMCHARS = '.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz'

def _next_term_ij(data, start=0):
  # find %blah or %(blah) in string data; returns (i,j) pair for s[i:j]"
  # used repeatedly in Madlibs.get()
  i = -1
  j = -1
  while i < 0 and j < 0:
    i = data.find('%', start)
    if (i+1 == len(data) or i < 0):
      i = -1
      break
    for bracepair in BRACEPAIRS:
      if data[i+1] == bracepair[0]:
        j = data.find(bracepair[1], i+2) + 1
    if j < i :
      if i+2 < len(data) and data[i:i+2] == '%%':
        return (i, i+2)
      j = i+1
      while j < len(data) and (data[j] in TERMCHARS) :
        j += 1
    if j == i+1:
      start = i+1
      i = -1
      j = -1
  return (i, j)

def _extract_terms(data):
  # "%alpha is a %beta with a huge %gamma" -> ['alpha', 'beta', 'gamma']
  terms = []
  (i, j) = (0, 0)
  (i, j) = _next_term_ij(data)
  while (i, j) != (-1, -1):
    term = data[i+1:j]
    if (term[0], term[-1]) in BRACEPAIRS :
      term = term[1:-1]
    terms.append(term)
    (i, j) = _next_term_ij(data, j)
  return terms

def _good_term(termname):
  # validate a term name
  # I'm trying to avoid importing re
  if not isinstance(termname, basestring):
    return False
  if not termname[0].isalpha():
    return False
  if not termname.replace('.','').replace('_','').isalnum() :
    return False
  return True


class Madlibs(object):
  """ Each instance of this class will have its own vocabulary of stories.
  Using it without a vocabulary initialized will return 'None' or
  raise a KeyError if you try to request something specific from the
  vocabulary.
  Be ready to catch madlibs.VocabularyError or TypeError or KeyError
  """

  def __init__(self, vocabulary=None) :
    " can pass a dict for vocabulary or filename to a vocabulary file "
    self.vocabulary = { '#':'', '@':[] }
    self.shuffles = {}
    self.errors = []
    self.warnings = []
    self.__cmp__ = self.vocabulary.__cmp__
    self.__iter__ = self.vocabulary.__iter__
    self.__contains__ = self.vocabulary.__contains__
    if vocabulary :
      self.load(vocabulary)

  def __del__(self):
    # if isinstance(self.vocabulary, shelve.Shelf):
    # can't use above, get 'NoneType' for the 'shelve' reference
    try:
      self.vocabulary.sync()
    except AttributeError:
      pass
    try:
      self.vocabulary.close()
    except AttributeError:
      pass

  def _is_valid(self):
    """ quick check of self.vocabulary for correctness of structure
    raises VocabularyError. use validate() method for diagnosing
    problems inside the data
    """
    if not isinstance(self.vocabulary, (dict, shelve.Shelf)):
      raise VocabularyError('vocabulary bad data type "%s"' % type(self.vocabulary))
    if not '@' in self.vocabulary :
      raise VocabularyError('term "@" is missing')
    for term in self.vocabulary.keys() :
      if term == '@' :
        if not isinstance(self.vocabulary['@'], list) :
          raise VocabularyError('term "@" is not a list')
        elif len(self.vocabulary['@']) == 0 :
          raise VocabularyError('term "@" is empty')
      elif term == '#' :
        if not isinstance(self.vocabulary.get('#',''), basestring):
          raise VocabularyError('term "#" is not a string')
      elif not _good_term(term) :
        raise VocabularyError('term "%s" is illegal' % term)
    return True

  def delterm(self, term):
    " for removing a term from the vocabulary "
    del(self.vocabulary[term])

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
    if isinstance(filenameordict, (dict, shelve.Shelf)):
      self.vocabulary = filenameordict
    elif isinstance(filenameordict, basestring) :
      try:
        self.vocabulary = shelve.open(filenameordict, flag='w')
      except anydbm.error:
        infile = open(filenameordict,'r')
        self.vocabulary = json.load(infile)
        infile.close()
    if self.vocabulary :
      self.__iter__ = self.vocabulary.__iter__
      self.__contains__ = self.vocabulary.__contains__
    return self._is_valid()

  def sync(self):
    " for when you used Madlibs.load(shelve.open()) "
    if isinstance(self.vocabulary, shelve.Shelf):
      return self.vocabulary.sync()
    elif 'sync' in dir(self.vocabulary):
      return self.vocabulary.sync()
    else:
      raise VocabularyError('vocabulary doesn\'t have sync() method')

  def save(self, filething):
    " saves the vocabulary state to file or file-object "
    if isinstance(self.vocabulary, shelve.Shelf):
      # also flush to disk
      self.vocabulary.sync()
    if isinstance(filething, basestring):
      filething = open(filething, 'w')
    if isinstance(filething, file):
      try:
        json
      except NameError:
        filething.write(str(self.vocabulary))
      else:
        json.dump(self.vocabulary, filething, sort_keys=True, indent=2)
      filething.close()
    else:
      raise TypeError("expected str or file object; received "+ type(filething))

  def validate(self):
    """ checks the vocabulary for problems
    returns False if problems are found ("valid == False")
    and populates self.errors and self.warnings as a list
    """
    # "too many branches (20/12)"  shut up, pylint
    self.errors = []   # side effects! hisssss!
    self.warnings = [] # side effects! hisssss!
    try:
      self._is_valid()
    except VocabularyError as err:
      self.errors.append(repr(err))
    terms = self.vocabulary.keys()
    terms.sort()
    termsseen = set()
    for term in terms:
      try:
        if term in '!$%^&*':
          # reserved, presently unused
          continue
        elif term == '@':
          for story in self.vocabulary['@']:
            termsseen.add(story)
            if not _good_term(story):
              self.errors.append('bad story Term \"%s\" in \'@\'' % story)
            if self.vocabulary.get(story) is None:
              self.errors.append('missing story Term \"%s\" in \'@\'' % story)
            for storyterm in self.vocabulary[story]:
              if not _extract_terms(storyterm) :
                self.warnings.append("no substitutions in \"%s\"" % storyterm)
        elif term == '#':
          # already checked with self._is_valid()
          pass
        else :
          values = self.vocabulary[term]
          if isinstance(values, basestring):
            values = [values,]
          if not isinstance(values, list):
            self.errors.append('term %s has unexpected value type "%s"' % (term, type(values)))
          elif len(values) == 0:
            self.errors.append('term "%s" has zero values' % term)
          else:
            for value in values:
              # someday, values will themselves be lists,
              # for terms like ['run', 'running', 'ran']
              termsseen.update(_extract_terms(value))
              try:
                blurb = self.story(value)
                (i, j) = _next_term_ij(blurb)
                if (i, j) != (-1, -1):
                  self.errors.append('term "%s" has unknown term "%s" in value "%s"' % (term, blurb[i:j], value))
              except (VocabularyError, StandardError) as err:
                self.errors.append('term "%s" has troublesome value "%s"; (%s)' % (term, str(value), str(err)))
      except (VocabularyError, StandardError) as err:
        self.errors.append('term "%s": %s' % (term, repr(err)))
    for term in terms:
      if len(term) > 1 and not term in termsseen :
        self.warnings.append('term "%s" is unused' % term)
    return len(self.errors) == 0

  def addterm(self, term, data=None):
    " for adding a new term to the vocabulary "
    if term in self :
      self.insert(term, data)
    elif not _good_term(term):
      raise TypeError('bad term; "%s"' % type(term))
    elif data == None:
      self.vocabulary[term] = []
    elif isinstance(data, basestring):
      self.vocabulary[term] = [data]
    elif isinstance(data, list):
      self.vocabulary[term] = list(data)
    else:
      raise TypeError('bad data; expected str or list; received '+ type(data))

  def insert(self, term, data=None):
    " for adding more values to a term in the vocabulary "
    if not isinstance(term, basestring):
      raise TypeError('bad term; expected str, got '+ type(term))
    if not term in self.vocabulary:
      self.addterm(term, data)
    elif isinstance(data, basestring):
      self.vocabulary[term].append(data)
    elif isinstance(data, list):
      # "why temp?" just in case self.vocabulary is shelve.Shelf
      temp = self.vocabulary[term]
      for i in data:
        temp.append(i)
      self.vocabulary[term] = temp
    else:
      raise TypeError('bad data; expected str or list, got '+ type(data))

  def __setitem__(self, term, data):
    "see insert()"
    self.insert(term, data)

  def remove(self, term, data):
    """ removes an item from a term
    The entire item must be included with marks intact and case-sensitive
    If the item isn't associated with this term, it will return False.
    """
    if not term in self.vocabulary:
      raise KeyError('term not found in vocabulary; '+ term)
    try:
      self.vocabulary[term].remove(data)
    except ValueError:
      return False
    return True

  def __len__(self):
    """how many random stories are available in the loaded vocabulary.
    This is not the same as how many terms are in the vocabulary.
    """
    leng = 0
    if len(self.vocabulary) == 0 :
      return None
    if not '@' in self.vocabulary :
      return leng
    for i in self.vocabulary['@']:
      try:
        if isinstance(self.vocabulary[i], basestring):
          leng += 1
        else:
          leng += len(self.vocabulary[i])
      except KeyError:
        leng += 0
    return leng

  def __getitem__(self, term):
    "see get()"
    return self.get(term)

  def get(self, term, default=None):
    """ returns a random item from that term in the vocabulary
    for convenience, given '(alpha|beta|gamma)' it will return
    a random choice from 'alpha' or 'beta' or 'gamma'
    single-character term is not allowed; will raise KeyError
    """
    if not isinstance(term, basestring):
      raise TypeError('bad term type '+repr(type(term)))
    if term[0] == '%':
      # in case we passed %fruit instead of 'fruit'
      term = term[1:]
    if not term :
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
      while (values == None and '.' in key) :
        key = key[:key.rindex('.')]
        values = self.vocabulary.get(key)
      if isinstance (values, basestring):
        values = [values,]

    value = default
    if values :
      if not self.shuffles.get(term) :
        self.shuffles[term] = list(range(len(values)))
        random.shuffle(self.shuffles[term])
      value = values[self.shuffles[term].pop()]

    return value

  def comments(self, data=None):
    " get/set comment text for the vocabulary "
    if data == None:
      return self.vocabulary.get('#')
    else:
      self.vocabulary['#'] = str(data)

  def templates(self, termlist=None):
    """ get/set which terms in the vocabulary are story templates
    terms provided must already exist in the vocabulary
    """
    if termlist == None :
      return self.vocabulary['@']
    elif isinstance(termlist, basestring):
      if not termlist in self.vocabulary:
        raise KeyError('bad template list; "'+termlist+'" not found in vocabulary')
      self.vocabulary['@'] = [termlist,]
    elif isinstance(termlist, list):
      for i in termlist:
        if not i in self.vocabulary:
          raise KeyError('bad template list; "'+i+'" not found in vocabulary')
      self.vocabulary['@'] = termlist
    else:
      raise ValueError('improper type "%s" for termlist' % type(termlist))

  def get_template(self, term=None, search=None):
    """ fetches a random template from the vocabulary.
    term: use this term; can be a list of terms
    search: only choose from the stories that have this substring
    """
    if self.vocabulary == None :
      return None
    if not '@' in self.vocabulary :
      raise VocabularyError("missing '@' term in vocabulary")
    if isinstance(term, basestring) :
      template_types = [term,]
    elif isinstance(term, list) :
      template_types = list(term)
    else:
      template_types = self.vocabulary['@']
    if search :
      stories = []
      for i in template_types:
        for j in self.vocabulary[i]:
          if j.find(search) >= 0 :
            stories.append(j)
      if len(stories) == 0:
        # no matches among the template_types we're supposed to use
        return None
      else:
        return random.choice(stories)
    else:
      return self.get(random.choice(template_types))

  def story(self, template=None):
    """ in template, replaces all the %(word1|word2|word3) with a
    random item and replaces %keyname with a random item from the
    vocab if template not provided, gets a new one from get_template()
    """
    if template == None or template == '@':
      template = self.get_template()
    if template == None:
      return None
    text = template
    bad_loop = []
    (i, j) = _next_term_ij(text, 0)
    old_j = -1
    while (i >= 0 and j > 0):
      if text[i:j] == '%%' :
        text = text[:i] + '%' + text[i+2:]
        (i, j) = _next_term_ij(text, i+3)
        continue
      vocabword = text[i+1:j] # doesn't pick up the %
      try:
        vocabword = self.get(vocabword)
      except KeyError as err:
        raise VocabularyError('bad template "%s"; (%s)' % (template, str(err)) )
      if (vocabword != None):
        text = text[:i] + vocabword + text[j:]
        (i, j) = _next_term_ij(text, i)
      else:
        (i, j) = _next_term_ij(text, i+1)
      if j > 0 and j <= old_j :
        bad_loop.append(vocabword)
        if len(bad_loop) > 5:
          raise VocabularyError('vocabulary loop detected '+ bad_loop )
      else:
        bad_loop = []
      old_j = j
    return text

class VocabularyError(Exception):
  """ For errors caused by misunderstanding the internal structure
  of the Madlibs vocabulary data; missing values, trying to add
  non-strings as terms, and so on.  Easier to catch this way.
  """


# madlibs.py
# encoding: utf8
# author: Mozai <moc.iazom@sesom>
# version: 20120929
""" Madlibs takes a dict as vocabulary of story-strings with marked spots
    for substituting random words or phrases from collections.   It is
    intended to be used iteratively, and uses a randomizing method
    intended for high novelty in the output.
    Looks like a dict() but each time you ask for the value of a key,
    you get something different from a list associate with that key.
    Has some helper methods, like knowing which keys are stories/ seeds.
    God this description is poor; look for a readme.txt with this.
"""

import random, shelve
try:
  import json
except ImportError:
  pass

# used for on-the-fly terms in stories. ie: %{red,cerulian,rust,cherry}
BRACEPAIRS = (('(', ')'), ('[', ']'), ('{', '}'), ('<', '>'), ('|', '|'))

def _next_term_ij(data, start=0):
  # find %blah or %(blah) in string data; returns (i,j) pair for s[i:j]"
  # used repeatedly in Madlibs.get()
  i = -1
  j = -1
  while i < 0 and j < 0:
    i = data.find('%', start)
    if (i+1 == len(data) or i < 0):
      break
    for bracepair in BRACEPAIRS:
      if data[i+1] == bracepair[0]:
        j = data.find(bracepair[1], i+2) + 1
    if j < i :
      if i+2 < len(data) and data[i:i+2] == '%%':
        return (i, i+2)
      j = i+1
      while j < len(data) and (data[j].isalpha() or data[j] in '_.') :
        j += 1
    if j == i+1:
      start = i+1
      i = -1
      j = -1
  return (i, j)

class Madlibs(object):
  """ Each instance of this class will have its own vocabulary of stories.
      Using it without a vocabulary initialized will return 'None' or
      raise a KeyError if you try to request something specific from the
      vocabulary.
      Be ready to catch madlibs.VocabularyError or TypeError or KeyError
  """

  def __init__(self, vocabulary=None) :
    " can pass a dict for vocabulary or filename to a vocabulary file "
    self.verb_suffixes = ('', 'ed', 'ing')
    self.vocabulary = {'@':list(), '#':str()}
    self.shuffles = dict()
    if vocabulary :
      self.load(vocabulary)

  def __del__(self):
    # if isinstance(self.vocabulary, shelve.Shelf):
    # can't use above, get 'NoneType' for the 'shelve' reference
    if 'close' in dir(self.vocabulary):
      self.vocabulary.close()

  def clear(self):
    "Empties the vocabulary"
    self.vocabulary = dict()
    self.shuffles.clear()

  def load(self, filenameordict):
    """ reads a vocabulary data set from filename or a dict object
    could raise exceptions from file.open() or json.load()
    """
    self.vocabulary = None
    if isinstance(filenameordict, (dict, shelve.Shelf)):
      self.vocabulary = filenameordict
    elif isinstance(filenameordict, (str, unicode)) :
      try:
        self.vocabulary = shelve.open(filenameordict, flag='w')
      except:
        infile = open(filenameordict,'r')
        try: json
        except NameError:
          self.vocabulary = eval(infile.read())
        else:
          self.vocabulary = json.load(infile)
        infile.close()
    if not isinstance(self.vocabulary, (dict, shelve.Shelf)):
      raise VocabularyError('bad vocabulary: loaded vocabulary seems empty')
    if not '@' in self.vocabulary :
      raise VocabularyError('bad vocabulary: no "@" item')
    if ((not isinstance(self.vocabulary['@'], list)) 
        or (len(self.vocabulary['@']) == 0)
       ) :
      raise VocabularyError('bad vocabulary: "@" item is not a list')
    if self.vocabulary :
      return True
    else:
      return False

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
    if isinstance(filething, (str, unicode)):
      filething = open(filething, 'w')
    if isinstance(filething, file):
      try: json
      except NameError:
        filething.write(str(self.vocabulary))
      else:
        json.dump(self.vocabulary, filething, sort_keys=True, indent=2)
      filething.close()
    else:
      raise TypeError("expected str or file object; received "+ type(filething))

  def validate(self):
    " checks the vocabulary for loops, missing terms, or unused terms "
    report = str()
    if len(self.vocabulary) == 0:
      report += 'vocabulary is empty.\n'
      return report
    if not '@' in self.vocabulary:
      report += 'vocabulary missing required term "@".\n'
    if '#' in self.vocabulary :
      comment = self.vocabulary['#']
      if not isinstance(comment, (str, unicode)):
        report += 'vocabulary term "#" is not string (type '+type(comment)+')\n'
    terms = list(self.vocabulary.keys())
    terms.sort()
    for term in terms:
      if term in '!@#$%^&*':
        continue
      values = self.vocabulary[term]
      if not isinstance(values, (list, str, unicode)):
        report += 'term "'+term+'" has unexpected value type "'+str(type(values))+'"\n'
        continue
      if len(values) == 0:
        report += 'term "'+term+'" has zero values\n'
        continue
      for value in values:
        try:
          self.story(value)
        except Exception as err:
          report += 'term "'+term+'" has troublesome value "'+value+'"; ('+str(err)+')\n'
    return report

  def addterm(self, term, data=None):
    " for adding a new term to the vocabulary "
    if term in self :
      self.insert(term, data)
    elif not isinstance(term, (str, unicode)):
      raise TypeError('bad term; expected str or unicode; received '+type(term))
    elif (not term[:1].isalpha()):
      raise KeyError('bad term; first byte "'+term[:1]+'" of "'+term+'" must be alpha')
    elif data == None:
      self.vocabulary[term] = list()
    elif isinstance(data, (str, unicode)):
      self.vocabulary[term] = [data]
    elif isinstance(data, (list, tuple)):
      self.vocabulary[term] = list(data)
    else:
      raise TypeError('bad data; expected str or list; received '+ type(data))

  def delterm(self, term):
    " for removing a term from the vocabulary "
    del(self.vocabulary[term])

  def __delitem__(self, term):
    self.delterm(term)

  def __iter__(self):
    return self.vocabulary.__iter__()

  def insert(self, term, data=None):
    " for adding more values to a term in the vocabulary "
    if not isinstance(term, (str, unicode)):
      raise TypeError('bad term; expected str, got '+ type(term))
    if not term in self.vocabulary:
      self.addterm(term, data)
    elif isinstance(data, (str, unicode)):
      self.vocabulary[term].append(data)
    elif isinstance(data, (list, tuple)):
      # "why temp?" just in case self.vocabulary is shelve.Shelf
      temp = self.vocabulary[term]
      for i in data:
        temp.append(i)
      self.vocabulary[term] = temp
    else:
      raise TypeError('bad data; expected str or list, got '+ type(data))

  def __setitem__(self, term, data):
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

  # do I make __iter__ ?  would it iterate over get_story to return just
  #  a random story item, or would it call madlibs() once for each possible
  #  story?

  def __len__(self):
    """how many random stories are available in the loaded vocabulary.
    This is not the same as how many terms are in the vocabulary.
    """
    leng = 0
    if len(self.vocabulary) == 0 : 
      return None
    if not '@' in self :
      return leng
    for i in self.vocabulary['@']:
      try:
        if isinstance(self.vocabulary[i], (str, unicode)):
          leng += 1
        else:
          leng += len(self.vocabulary[i])
      except KeyError:
        leng += 0
    return leng

  def __contains__(self, key):
    " returns True if vocabulary has this term "
    return self.vocabulary.__contains__(key)

  def __getitem__(self, term):
    return self.get(term)

  def get(self, term, default=''):
    """ returns a random item from that term in the vocabulary
        for convenience, given '(alpha|beta|gamma)' it will return
        a random choice from 'alpha' or 'beta' or 'gamma'
        single-character term is not allowed; will raise KeyError
    """
    # pylint complains 'too many branches(20/12)'  whatever, pylint
    if not isinstance(term, (str, unicode)):
      raise TypeError('bad term type; expected str, got '+type(term))
    if term[0] == '%':
      # in case we passed %fruit instead of 'fruit'
      term = term[1:]
    if term == '':
      # why does this happen? shouldn't.
      return default
    if self.vocabulary == None :
      raise VocabularyError('vocabulary not initialized')
    if (term[:1], term[-1:]) in BRACEPAIRS:
      term = term[1:-1]
    if '|' in term:
      # it's %(alpha|beta|gamma) type
      # TODO: way to escape \| for %(alpha\|a|beta\|b|gamma\|c)
      values = term.split('|')
      if ((not term in self.shuffles) or len(self.shuffles[term]) == 0):
        self.shuffles[term] = list(range(len(values)))
        random.shuffle(self.shuffles[term])
      value = values[self.shuffles[term].pop()]
      return value
    # else it's %fruitcolour type
    key = term
    value = None
    while (len(key) > 0 and value == None):
      try:
        value = self.vocabulary[key]
      except KeyError:
        if '.' in key:
          key = key[:key.rindex('.')]
        else:
          key = ''
    if value == None:
      return ''
    elif isinstance(value, (str, unicode)):
      return value
    elif isinstance(value, (list, tuple)) :
      if len(value) == 0:
        # what is proper if a term has an empty list?
        value = ''
      if (not key in self.shuffles) or (len(self.shuffles[term]) == 0) :
        self.shuffles[term] = list(range(len(value)))
        random.shuffle(self.shuffles[term])
      value = value[self.shuffles[term].pop()]
    else:
      raise VocabularyError("bad vocabulary; item" + term +
                            "points to data type" + type(value))
    if isinstance(value, (list, tuple)):
      # we picked a list/tuple? probably verb tenses list then
      if term != key and term[len(key)+1:].isdigit() :
        j = int(term[len(key)+1:])
        value = value[j]
    return value

  def comments(self, data=None):
    " get/set comment text for the vocabulary "
    if data == None:
      if '#' in self.vocabulary:
        return self.vocabulary['#']
      else:
        return None
    else:
      self.vocabulary['!'] = str(data)

  def templates(self, termlist=None):
    """ get/set which terms in the vocabulary are story templates
    terms provided must already exist in the vocabulary
    """
    if termlist == None :
      return self.vocabulary['@']
    elif isinstance(termlist, (str, unicode)):
      if not termlist in self.vocabulary:
        raise KeyError('bad template list; "'+termlist+'" not found in vocabulary')
      self.vocabulary['@'] = [termlist,]
    elif isinstance(termlist, (list, tuple)):
      for i in termlist:
        if not i in self.vocabulary:
          raise KeyError('bad template list; "'+i+'" not found in vocabulary')
      self.vocabulary['@'] = termlist

  def get_template(self, term=None, search=None):
    """ fetches a random template from the vocabulary.
        term: use this term; can be a list of terms
        search: only choose from the stories that have this substring
    """
    if self.vocabulary == None :
      return None
    if not '@' in self:
      raise VocabularyError("missing '@' term in vocabulary")
    if isinstance(term, (str, unicode)) :
      template_types = [term]
    elif isinstance(term, (list, tuple)) :
      template_types = list(term)
    else:
      template_types = list(self.vocabulary['@'])
    # commenting out the following; gonna trust the user
    #for i in template_types :
    #  if not i in self.vocabulary['@'] :
    #    raise KeyError("term is not a valid story template; "+ term)
    if search :
      stories = list()
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
    """ in template, replaces all the |word1,word2,word3| with a random item
        and replaces |keyname| with a random item from the vocab mapping
        if template not provided, gets a new one from get_template()
    """
    if template == None:
      template = self.get_template()
    if template == None:
      return None
    text = template
    bad_loop = list()
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
        raise VocabularyError('bad template "%s"; (%s)', (template, str(err)) )
      text = text[:i] + vocabword + text[j:]
      (i, j) = _next_term_ij(text, i)
      if j > 0 and j <= old_j :
        bad_loop.append(vocabword)
        if len(bad_loop) > 5:
          raise VocabularyError('vocabulary loop detected '+ bad_loop )
      else:
        bad_loop = list()
      old_j = j
    return text

class VocabularyError(Exception):
  """ For errors caused by misunderstanding the internal structure
  of the Madlibs vocabulary data; missing values, trying to add
  non-strings as terms, and so on.  Easier to catch this way.
  """


if __name__ == '__main__':
  # test suite goes here
  VFILE = 'test.json'
  print("testing madlibs.py with", VFILE)
  ML = Madlibs(VFILE)
  if ML.load(VFILE):
    print VFILE , " loaded; " , len(ML) , "stories."
    print '' 

    print "validating vocabulary..."
    REPORT = ML.validate()
    if REPORT == '':
      print "no problems; forgot to put a bad term in there, boss?"
    else:
      print "found your bait boss; make sure it's the correct bad stuff"
      print REPORT
    print ''

    print "test run of 3x the stories in" , VFILE
    for I in range(3*len(ML)):
      print "..." , ML.story()
    print ''

  else:
    print VFILE , "did not load."


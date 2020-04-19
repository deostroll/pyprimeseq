import gmpy2
from pprint import pprint as pp

def sqrt_test(N):
  n = N
  while True:
    root, remainder = gmpy2.isqrt_rem(n)
    if remainder != 0:
      break
    n = root
  return gmpy2.is_prime(n)

class RIterator:
  def __init__(self, store = False):
    self.num_list = []
    self.store = store
  
  def __iter__(self):
    self.n = gmpy2.mpz(1)
    return self

  def __next__(self):
    n = self.n

    while True:
      if n == 1:
        n = gmpy2.add(n, 1)
        continue
      elif sqrt_test(n) == False:
        if self.store:
          self.num_list.append(n)
        self.n = gmpy2.add(n, 1)
        return n
      n = gmpy2.add(n, 1)

class P2n_1:
  def __init__(self, start):
    self.start = start
    self.iterator = None
    
  def __iter__(self):
    if gmpy2.is_prime(self.start):
      self.s = 0
    else:
      raise Exception("Invalid prime:", self.start)
    return self

  def __next__(self):
    result = self.start ** ((2 ** self.s) - 1)
    # result = gmp
    self.s += 1
    return result

  def get_iterator(self):
    if self.iterator is None:
      self.iterator = iter(self)
    return self.iterator

  def reset_iterator(self):
    self.iterator = iter(self)
    return self.iterator

class RDict(dict):
  def __init__(self, *args):
    dict.__init__(self, args)
    ri = RIterator()
    _iter = iter(ri)
    self._iterator = _iter
    self.add_next()
  
  def add_next(self, until = None):
    _iter = self._iterator
    for x in range(0, 100):
      value = next(_iter)
      dict.__setitem__(self, value, { 'used' : False })
      if until is not None and value >= until:
        break
    return value


  def __missing__(self, key):
    while True:
      nxt = self.add_next(key)
      if nxt >= key:
        break
    return dict.__getitem__(self, key) if nxt == key else None

def nf2n(p, n):
  return gmpy2.mpz(p) ** 2 ** n

def nf2n_1(p, n):
  return gmpy2.mpz(p) ** ((2 ** n) - 1)

def serial_gen(n = 0):
  while True:
    yield n
    n += 1

class NC:
  """
  Number container class
  """
  display = False
  threshold = 10 ** 10
  def __init__(self, n):
    self.n = n
  def __str__(self):
    return str(self.n)
  def __repr__(self):
    if NC.display:
      f = gmpy2.mpfr(self.n)
      t = gmpy2.digits(f, 10, 5)
      return '0.%se%s' % (t)
    elif self.n/NC.threshold < 1:
      return str(self.n)
    else:
      return '<BIG_NUM>'

def series_terms_enumerator(prime, start = 0, list_size = 3):
  return [ ( \
              prime,                    \
              n,
              NC( nf2n(prime, n) ),     \
              NC( nf2n_1(prime, n) )    \
            ) for n in range(start, start + list_size)]
      
# =========

# n = 3
# # p2 = [ ( 2, n, NumContainer(nf2n(2, n)), NumContainer(nf2n_1(2, n)) ) for n in range(0, n + 1 ) ]
# p2 = [ ( 2, n, nf2n(2, n), nf2n_1(2, n) ) for n in range(0, n + 1 ) ]

# pp(p2)

# x1 = p2[1][3]
# x2 = p2[2][3]
# print(list(range(x1, x2)))
# rdict = RDict()
# sep = "=" * 10
# length = len(p2)
# for x in range(1, len(p2)):
#   curr = p2[x]
#   prev = p2[x - 1]

#   low = prev[3]
#   high = curr[3]

#   if high - low - 1 > 0:
#     for y in range(low + 1, high):
#       v = 2 * y
#       # print(v , rdict[v])
#       q = rdict[v]
#       q['used'] = True
#       q['start'] = low
#       q['end'] = high
  
#   # print(sep)

# # pp(rdict.items())
# res = filter(lambda t: t[1]['used'] == False, rdict.items())
# pp(dict(res))

# =================
p = 2
p2_0_2 = series_terms_enumerator(p)

pp(p2_0_2)

p2_3_5 = series_terms_enumerator(p, 3)

pp(p2_3_5)

p2_0_5 = series_terms_enumerator(p, list_size=5)
pp(p2_0_5)
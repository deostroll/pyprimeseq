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



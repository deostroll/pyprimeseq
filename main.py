import gmpy2

class PIter:
  def __init__(self):
    self.num_list = []

  def __iter__(self):
    self.n = 1
    return self

  def __next__(self):
    while not is_prime(self.n):
      self.n += 1
    
    self.num_list.append(self.n)
    num = self.n
    self.n += 1
    return num

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

class P2n:
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
    result = self.start ** 2 ** self.s
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

def gen_terms(iterator, terms):
  return [ next(iterator) for x in range(0, terms)]

r_iterator = RIterator()
riter = iter(r_iterator)

p2 = P2n(2)
p2iter = p2.get_iterator()

p2_1 = P2n_1(2)
p2n_1iter = p2_1.get_iterator()

r_terms = gen_terms(riter, 10)
p2n_terms = gen_terms(p2iter, 10)
p2n_1_terms = gen_terms(p2n_1iter, 10)
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

def PrimeGen(n = 2):
  while True:
    if gmpy2.is_prime(n):
      yield n
    n += 1

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
      dict.__setitem__(self, value, { 'used': False })
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
              n,                        \
              NC( nf2n(prime, n) ),     \
              NC( nf2n_1(prime, n) )    \
            ) for n in range(start, start + list_size)]

def PrimeGenLimit(limit):
  p = PrimeGen()
  _yield = next(p)
  while _yield <= limit:
    yield _yield
    _yield = next(p)

def series_synthesize(series, rdict):
  term0 = series[0]
  prime_seed = term0[0]
  length = len(series)

  for x in range(1, length):
    curr = series[x]
    prev = series[x - 1]
    low = prev[3].n
    high = curr[3].n

    if high - low - 1 > 0:
      for y in range(low + 1, high):
        term = (prime_seed, y)
        value = prime_seed * y
        r = rdict[value]
        if 'hits' in r.keys():
          r['hits'].append(term)
        else:
          hits = []
          for prime in PrimeGenLimit(prime_seed):
            if value % prime == 0:
              hits.append((prime, value//prime))
          r['hits'] = hits
          r['used'] = True




      
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

# ================= 2020-04-19 10:22:00 - testing series enumerator
# p = 2
# p2_0_2 = series_terms_enumerator(p)

# pp(p2_0_2)

# p2_3_5 = series_terms_enumerator(p, 3)

# pp(p2_3_5)

# p2_0_4 = series_terms_enumerator(p, list_size=5)
# pp(p2_0_4)

# ================= 2020-04-19 10:22:28 - test PrimeGen

# gen = PrimeGen()

# print([ next(gen) for x in range(0, 10)])

# gen2 = PrimeGen(10)
# print([ next(gen2) for x in range(0, 10)])

# ================= 2020-04-19 10:44:47 - test prime gen limit

# p = 13

# g = PrimeGenLimit(p)

# print([ x for x in g ])

# ================= 2020-04-19 10:56:47 - testing synthesizer

# rdict = RDict()
# p2_0_2 = series_terms_enumerator(2)
# pp(p2_0_2)

# series_synthesize(p2_0_2, rdict)

# p3_0_3 = series_terms_enumerator(3)
# pp(p3_0_3)

# series_synthesize(p3_0_3, rdict)

# p5_0_5 = series_terms_enumerator(5)
# pp(p5_0_5)

# series_synthesize(p5_0_5, rdict)

# pp(rdict)

# ================= 2020-04-19 12:40:07 - testing the synthesizer over a pre-generated prime set

def n_prime_generator(n):
  g = PrimeGen()
  for x in range(0, n):
    yield next(g)

def main(n, t):
  rdict = RDict()
  for p in n_prime_generator(n):
    series = series_terms_enumerator(p, list_size=t)
    pp(series)
    series_synthesize(series,rdict)
  pp(rdict)

if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser(description='Tracks the residual terms for prime series')
  parser.add_argument('-n', '--size', help='Compute for the first n primes', type=int, metavar='size')
  parser.add_argument('-t', '--terms', help='Number of terms to compute for each prime series', type=int, metavar='terms')

  args = parser.parse_args()
  main(args.size, args.terms)

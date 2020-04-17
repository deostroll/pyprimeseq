import math
import matplotlib.pyplot as plt
import numpy as np
import gmpy2

def is_prime(n):
  if n == 1:
    return False
  elif n == 2:
    return True
  elif n > 2 and n % 2 == 0:
    return False
  m = math.floor(math.sqrt(n))
  for x in range(3, m + 1, 2):
    if n % x == 0:
      return False
  return True

class PrimeIter:
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

# CONST = (1 / math.log(2))
def calculate_n(p, N):
  return  (1 / math.log(2)) * math.log(math.log(N)/math.log(p))

# primes = PrimeIter()
# piter = iter(primes)

# val = 17 ** 3
# print('Number:', val)

def generate_data(size, num):
  data = []
  prime_iterator = PrimeIter()
  _iter = iter(prime_iterator)
  
  for i in range(0, size):
    p = next(_iter)
    n = calculate_n(p, num)
    data.append([p,n])
  
  return data

def plot(N, size):
  data = generate_data(size, N)
  x = np.arange(1, len(data) + 1)
  y = np.array(data)[:, 1]

  plt.plot(x, y)
  plt.show()
  return data

def is_in_interval(n, percentage):
  i = (n * 1 - percentage, n * 1 + percentage)
  return n > i[0] and n < i[1]

def sqrt_test(N):
  n = N
  while True:
    root, remainder = gmpy2.isqrt_rem(n)
    if remainder != 0:
      break
    n = root
  return gmpy2.is_prime(n)

class RSeqIterator:
  def __init__(self):
    self.num_list = []
  
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
        self.num_list.append(n)
        self.n = gmpy2.add(n, 1)
        return n
      n = gmpy2.add(n, 1)

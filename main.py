from wordlist import wordlist
from shamir import Shamir
from hashlib import sha256
t = 3
n = 3

# key = ['joke', 'notable', 'empower', 'cage', 'expand', 'grab', 'lecture', 'spray', 'dice', 'figure', 'february', 'auto']

key = "brass cruise talent human social retire problem toe bring swim team remove".split(" ")
print("your key is: " + str(key))
print("----------------")
print(list(map(lambda x: wordlist.index(x), key)))

def get_integer_from_key(key):
    key[-1] = key[-1] >> 4 # take the first 7 bits of the last word

    s = 0
    for i in range(0, len(key)-1):
      s = s + (key[i] << (128 - ((i+1) * 11)))
    
    s += key[-1]
    return s

def get_checksum(nb):
    # takes a number of size 128 bits and hashes it with sha256
    # returns the first 4 bits as a number
    #take the first 1 byte from the hash of nb
    bytes_object = bytes(to_list_of_ints(nb, 128, 8))
    b = sha256(bytes_object).digest()[0]

    # take the first 4 bits of the 1 byte
    b = b >> 4
    return b

def append_checksum(nb_key, checksum):
  # adds the 4 bit checksum to the of 128 bit key 
  return (nb_key << 4) + checksum

def to_list_of_ints(nb, total, word_size):
  # takes a 132 bit number and produces a list of 11 bit integers
  word_count = total//word_size
  def special_sum(arr):
    # shift and add
    s = 0
    for i in range(0, len(arr)):
      s += (arr[i] << (word_count - i - 1) * word_size)
    return s

  l = [0 for i in range(0, word_count)]
  l[0] = nb >> word_size * (word_count - 1)

  for i in range(1, word_count):
    l[i] = (nb - special_sum(l[0:i])) >> ((word_count - i - 1) * word_size)
  return l

key = list(map(lambda x: wordlist.index(x), key))
nb = get_integer_from_key(key)
checksum = get_checksum(nb)

rec = (nb << 4) + checksum
print(to_list_of_ints(rec, 132, 11))

shares = Shamir.split(t, n, nb)
shares = [to_list_of_ints((share[1]._value << 4) + get_checksum(share[1]._value), 132, 11) for share in shares]
print([[wordlist[index_word] for index_word in share] for share in shares])


# reconstruction
print("reconstruction:")
rec = [(i+1, get_integer_from_key(shares[i])) for i in range(0, len(shares))]
reconstructed = Shamir.combine(rec)._value
reconstructed_final_int = (reconstructed << 4) + get_checksum(reconstructed)
l = to_list_of_ints(reconstructed_final_int, 132, 11)
print([wordlist[l[i]] for i in range(0, len(l))])




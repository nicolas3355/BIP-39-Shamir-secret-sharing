from wordlist import wordlist
from shamir import Shamir
from hashlib import sha256
from Cryptodome.Random import get_random_bytes as rand_bytes
from Cryptodome.Util.number import bytes_to_long


def get_integer_from_key(ENT, key):
    # takes a list of integers each of size 11 bits
    # and constructs one big intger of size ENT
    l = key[-1] >> ENT//32  # discard the checksum from the last word

    s = 0
    for i in range(0, len(key)-1):
        s = s + (key[i] << (ENT - ((i+1) * 11)))
    s += l
    return s


def calculate_checksum(ENT, nb):
    # takes a number of size ENT bits and hashes it with sha256
    # returns the first ENT//32 bits of the hash as an integer
    bytes_object = bytes(to_list_of_ints(nb, ENT, 8))
    b = sha256(bytes_object).digest()[0]

    b = b >> (8 - ENT//32)
    return b


def append_checksum(ENT, nb_key, checksum):
    # adds the checksum of size EMT//32 to the secret key nb_key
    return (nb_key << ENT//32) + checksum

def is_seed_valid(mneumonic_seed):
    # checks that the list of words are generated correctly
    # by checking the checksum

    ENT = len(mneumonic_seed) * 11 - (len(mneumonic_seed) * 11)//32
    seed_int = list(map(lambda x: wordlist.index(x), mneumonic_seed))

    last_word = seed_int[-1]
    mask = (1 << ENT//32) - 1
    extracted_checksum = last_word & mask
 
    seed_big_int = get_integer_from_key(ENT, seed_int)
    calculated_checksum =  calculate_checksum(ENT, seed_big_int)
    return extracted_checksum == calculated_checksum

def to_list_of_ints(nb, total, word_size):
    # takes a (ENT + ENT//32) size bit number and produces
    # a list of 11 bit integers
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


def split_seed(t, n, mneumonic_seed):
    ENT = len(mneumonic_seed) * 11 - (len(mneumonic_seed) * 11)//32
    seed_int = list(map(lambda x: wordlist.index(x), mneumonic_seed))
    seed_big_int = get_integer_from_key(ENT, seed_int)
    shares = Shamir.split(t, n, seed_big_int, ENT)
    shares = [(share[0], to_list_of_ints((share[1]._value << (ENT//32)) +
              calculate_checksum(ENT, share[1]._value), ENT + ENT//32, 11))
              for share in shares]
    shares = [(share[0], [wordlist[index_word] for index_word in share[1]])
              for share in shares]
    return shares


def generate_random_seed(ENT):
    rnd = bytes_to_long(rand_bytes(ENT//8))
    checksum = calculate_checksum(ENT, rnd)
    seed_number = (rnd << ENT//32) + checksum
    l = to_list_of_ints(seed_number, ENT + ENT//32, 11)
    return [wordlist[l[i]] for i in range(0, len(l))]


def combine(shares):
    ENT = len(shares[0][1]) * 11 - (len(shares[0][1]) * 11)//32
    shares = [(share[0], list(map(lambda x: wordlist.index(x), share[1])))
              for share in shares]
    rec = [(share[0], get_integer_from_key(ENT, share[1]))
           for share in shares]
    reconstructed = Shamir.combine(rec, ENT)._value
    reconstructed_final_int = ((reconstructed << ENT//32) +
                               calculate_checksum(ENT, reconstructed))
    l = to_list_of_ints(reconstructed_final_int, ENT + ENT//32, 11)
    return ([wordlist[l[i]] for i in range(0, len(l))])

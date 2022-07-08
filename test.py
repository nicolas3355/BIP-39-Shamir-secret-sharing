from main import generate_random_seed, split_seed, combine
from random import randrange as rand


def test(nb_words):
    for i in range(0, 1000):
        n = rand(2, 10)
        t = rand(1, n)
        seed = generate_random_seed(128)
        print(seed)
        shares = split_seed(t, n, seed)
        print(shares)
        rec = combine(t, n, shares)
        print(rec)
        assert(all(map((lambda x: x[0] == x[1]), zip(seed, rec))))


test(12)

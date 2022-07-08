from main import generate_random_seed, split_seed, combine
from random import randrange as rand


field_sizes = [128, 160, 192, 224, 256]


def test(number_of_trials):
    for i in range(0, number_of_trials):
        n = rand(2, 10)
        t = rand(1, n)
        seed = generate_random_seed(field_sizes[rand(0, len(field_sizes))])
        shares = split_seed(t, n, seed)
        rec = combine(t, n, shares)
        assert(all(map((lambda x: x[0] == x[1]), zip(seed, rec))))

test(1000)

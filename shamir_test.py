from main import generate_random_seed, split_seed, combine
from random import sample, randrange as rand


field_sizes = [128, 160, 192, 224, 256]

def test():
    number_of_trials = 1000
    for i in range(0, number_of_trials):
        n = rand(2, 10)
        t = rand(1, n)
        seed = generate_random_seed(field_sizes[rand(0, len(field_sizes))])
        shares = split_seed(t, n, seed)

        # sample t random shares
        t_shares = sample(shares, t)
        rec = combine(t_shares)
        # the t shares should reconstruct to the original seed
        assert(all(map((lambda x: x[0] == x[1]), zip(seed, rec))))

        # sample another t random shares
        t_shares = sample(shares, t)
        rec = combine(t_shares)
        # the t shares should reconstruct to the original seed
        assert(all(map((lambda x: x[0] == x[1]), zip(seed, rec))))
test()

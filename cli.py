from wordlist import wordlist
from main import is_seed_valid, split_seed, combine

options = ["split a seed", "reconstruct shares"]
seed_length = [12, 15, 18, 21, 24]
def user_options():
    print("Please choose:")
    for idx, element in enumerate(options):
        print("{}) {}".format(idx+1,element))
    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return int(i) 
    except:
        pass
    return None

def select_seed_length():
    print("Select your seed length:")
    for idx, element in enumerate(seed_length):
        print("{}) {}".format(idx+1,element))
    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return seed_length[int(i)-1]
    except:
        pass
    return None

def select_words(nb, is_share, n=None):
    words = []
    if(is_share):
        share_number = int(input("Please enter share number: "))
        assert(share_number <= n), "Share number must be between 1 and " + str(n)

    print("Please enter your mnemonic seed:")
    for idx in range(1, nb+1):
        word = input("Please enter word number " + str(idx)+": ").strip()
        if word not in wordlist:
            raise Exception("word must be in word list")
        words.append(word)
    # check the checksum whether it's correct or not
    assert (is_seed_valid(words)), "invalid checksum"
    print("You have successfully entered you mnemonic seed phrase")

    if is_share:
        return (share_number, words)
    return words

def select_thresholds():
    t = int(input("Please enter the minimum number of shares needed to reconstruct: "))
    n = int(input("Please enter the total number of shares: "))
    assert (t <= n), "the total number of shares must be greater than or equal to the number of shares needed for reconstruction"
    return (t, n)


def cli():
    choice = user_options()
    if(choice == 1):
        t, n = select_thresholds()
        nb = select_seed_length()
        words = select_words(nb, False)
        print(words)
        print(split_seed(t, n, words))
        

    elif(choice == 2):
        t, n = select_thresholds()
        nb = select_seed_length()
        shares = []
        for i in range(0, t):
            shares.append(select_words(nb, True, n))
        print(shares)
        print(combine(t, n, shares))

cli()


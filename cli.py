import argparse
from wordlist import wordlist
from main import is_seed_valid, split_seed, combine, generate_random_seed

quote = "\""

def split(mnemonic, total_shares, required_shares):
    mnemonic = mnemonic.split(" ")
    if not is_seed_valid(mnemonic):
        print("Invalid mnemonic seed.")
        return None
    shares = split_seed(required_shares, total_shares, mnemonic)
    return shares

def recover_seed(shares):
    formatted_shares = []
    for i, share in shares:
        share = share.split(" ")
        if not is_seed_valid(share):
            print(f"Invalid share {i} : {share}")
            return None
        formatted_shares.append((i, share))
    secret = combine(formatted_shares)
    return ' '.join(secret)

def gen_seed(seed_length):
    choices = [12, 15, 18, 21, 24]
    if(seed_length not in choices):
        print("invalid mnemonic length. you choices must be one of the following: 12, 15, 18, 21, 24")
    ENT = seed_length * 11 - (seed_length * 11)//32
    return generate_random_seed(ENT)



def main():
    parser = argparse.ArgumentParser(description="Split and recover a mnemonic seed")
    subparsers = parser.add_subparsers(dest="command")

    split_parser = subparsers.add_parser("split", help="Split a mnemonic seed into shares")
    split_parser.add_argument("-m", "--mnemonic", required=True, help="Mnemonic seed to split")
    split_parser.add_argument("-t", "--total", type=int, required=True, help="Total number of shares to generate")
    split_parser.add_argument("-r", "--required", type=int, required=True, help="Number of shares required to recover the seed")

    recover_parser = subparsers.add_parser("recover", help="Recover a mnemonic seed from shares")
    recover_parser.add_argument("-i", "--indexes", type=int, nargs='+', required=True, help="The shares indexes in order starting from (starting from 0)")
    recover_parser.add_argument("-s", "--shares", nargs='+', required=True, help="Shares to use for recovery")

    split_parser = subparsers.add_parser("gen", help="Generates a mnemonic seed")
    split_parser.add_argument("-n", "--number", type=int, required=True, help="Total number of words in the mnemonic seed")

    args = parser.parse_args()

    if args.command == "split":
        shares = split(args.mnemonic, args.total, args.required)
        for share in shares:
            share_index, share = share
            print(f" ({share_index},{quote}{' '.join(share)}{quote})")
    elif args.command == "recover":
        if(len(args.indexes) != len(args.shares)):
            print("the number of indexes should match the number of shares")
        l = []
        for i in range(0, len(args.indexes)):
            l.append((args.indexes[i], args.shares[i]))
        secret = recover_seed(l)
        print(f"Recovered secret: {secret}")
    elif args.command == "gen":
        secret = gen_seed(args.number)
        secret = " ".join(secret)
        print(f"Mnenomic seed: {quote}{secret}{quote}")
    else:
        print("Invalid command. Use 'split' or 'recover'.")

if __name__ == "__main__":
    main()


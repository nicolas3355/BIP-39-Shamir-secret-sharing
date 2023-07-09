# Shamir secret sharing for BIP32 mnemonic seeds
This is a command line interface (CLI) that allows you to split a mnemonic seed into shares using Shamir's Secret Sharing Scheme. This tool also allows you to recover the mnemonic seed from the shares. 


## Installation
This project requires poetry. A guide on how to install poetry can be found [here](https://python-poetry.org/docs/#installation)

## To run the tests:
`poetry run pytest`

## Usage
To use the tool, the script cli.py is the file to go. 

### Splitting a Seed
To split a seed into shares, use the `split` command. You will need to provide the mnemonic seed you want to split (`-m`), the total number of shares to generate (`-t`), and the number of shares required to recover the seed (`-r`). 

Here is an example of how to split a seed:

```
python cli.py split --mnemonic "obvious shoe liberty excess hobby primary mass gap sister earth rally cancel until armor dice" --total 5 --required 3
```

This command splits the given mnemonic seed into 5 shares, and any 3 of these shares can be used to recover the original seed.

### Recovering a Seed
To recover a seed from shares, use the `recover` command. You will need to provide the index of the shares you want to use for recovery (`-i`) and the actual shares (`-s`).

Here is an example of how to recover a seed:

```
python cli.py recover --indexes 1 2 3 --shares "share1" "share2" "share3"
```

Replace `"share1" "share2" "share3"` with the actual shares.

### Generating a seed 
To generate a seed, use the `gen` command. You will need to provide the number of words needed to produce your mnemonic seed (`-n`). You have a choice between 12, 15, 18, 21, 24.

Here is an example of how to generate a seed:

```
python cli.py gen -n 12
```


## Note

Additionally, the script includes an `is_seed_valid` function for verifying the validity of a mnemonic seed before splitting it.

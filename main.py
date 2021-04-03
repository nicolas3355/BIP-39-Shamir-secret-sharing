from wordlist import wordlist
from shamir import Shamir
t = 3
n = 3

key = ['joke', 'notable', 'empower', 'cage', 'expand', 'grab', 'lecture', 'spray', 'dice', 'figure', 'february', 'auto']
print("your key is: " + str(key))
print("----------------")

key = map(lambda x: wordlist.index(x), key)


shares = list(map(lambda x: Shamir.split(n, t, x), key))
nice_shares = [[] for i in range(n)]
for share in shares:
  for i in range(len(nice_shares)):
    nice_shares[i].append(wordlist[share[i][1]])
    # nice_shares[i].append(share[i][1])


for i in range(len(nice_shares)):
  print("share number " + str(i) +":" + str(nice_shares[i]))

print("----------------")
print("reconstructing:")
rec = []
for i in range(0, len(nice_shares[0])):
  rec.append(wordlist[Shamir.combine([ (j+1, wordlist.index(nice_shares[j][i])) for j in range(t)])])

print(rec)



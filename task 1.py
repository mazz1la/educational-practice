J = str("ab")
S = str("aabbccd")
count = 0
for i in S:
    if i in J:
        count += 1
print(count)
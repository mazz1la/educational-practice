from itertools import combinations

def comb_sum(candidates, target):
    result = set()


    for number in candidates:
        if number == target:
            result.add((number,))


    for r in range(2, len(candidates) + 1):
        for combo in combinations(candidates, r):
            if sum(combo) == target:
                result.add(combo)

    return list(result)

candidates = [10,1,2,7,6,1,5]
target = 8
combinations_found = comb_sum(candidates, target)
print(combinations_found)
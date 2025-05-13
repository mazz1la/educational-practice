def contains_duplicate(nums):
    seen = []
    for num in nums:
        if num in seen:
            return True
        seen.append(num)
    return False

nums = [1, 2, 3, 4]
print(contains_duplicate(nums))

nums2 = [1,1,1,3,3,4,3,2,4,2]
print(contains_duplicate(nums2))

nums3 =  [1,2,3,1]
print(contains_duplicate(nums3))



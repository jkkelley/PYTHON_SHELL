"""
    Given a non-empty array of integers nums,
    every element appears twice except for one.
    Find that single one.

    You must implement a solution with a linear
    runtime complexity and use only constant extra space.
"""

# nums = [2,2,1]
# Exoected Output: 1

nums = [4,1,2,1,2]

def singleNumer(nums):

    # No nested for loops
    # No arrays, hashmaps, they cause extra space

    print(5 ^ 5)

    result = 0

    for num in nums:
        result = result ^ num
        # print(result)
    return result
         

print(singleNumer(nums=nums))